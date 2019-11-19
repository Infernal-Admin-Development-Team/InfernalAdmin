import os
import subprocess
from pathlib import Path

from discord.ext.commands import Cog, command, check, MissingRequiredArgument, CommandInvokeError
from github import Github

from database import clear_db
from util import *


def pull_updates(branch):
    """
    Kicks off the update script on windows, on linux it puts the neccessary information in a file
    so the bot handler can update us after we die.
    """
    if CONFIG.os == "windows":
        cwd = Path(os.getcwd())
        parent = cwd.parent
        os.chdir(str(parent))

        subprocess.Popen(["python", 'update_windows.py', branch], shell=True)
    with open("branch.txt", "w+") as f:
        f.write(branch)
    f.close()


class AutoUpdate(Cog):
    """The AutoUpdate module contains everything needed to perform git operations on the bot
    it allows you to change the branch the bot is running on (to allow for easy testing of different branches)
    it also contains the check_for_updates task which is used in the production bot.
    """

    def __init__(self, bot):
        self.bot = bot

    def get_branch_names(self):
        """Gets the list of branches on the git repo"""
        g = Github()
        repo = g.get_repo(CONFIG.version_control.repo)
        ret_list = []
        for b in repo.get_branches():
            ret_list.append(b.name)
        return ret_list

    @command()
    @check(is_owner)
    async def branches(self, ctx):
        """->Gets the branches from the github repo"""
        out_str = " "
        branches = self.get_branch_names()

        for b in branches:
            out_str += b + "\n "
        await ctx.send("There are " + str(len(branches)) + " branches\n```" + out_str + "```")


    @command()
    @check(is_owner)
    async def update(self, ctx, branch: str):
        """->Causes the bot to update its local files to match the branch of your choosing"""

        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.message.channel

        if branch not in self.get_branch_names():
            return await ctx.send("Invalid branch")
        reply = await ctx.send("Are you sure you want to update the bot to ``" + branch + "``")
        setattr(ctx, 'reply', reply)
        msg = await self.bot.wait_for('message', timeout=20, check=check)
        if "y" in msg.content:
            # kick off the update script and die
            await ctx.send("Updating to ``" + branch + "``")
            if CONFIG.os == "windows":
                await ctx.send(
                    "If your bot fails to start after the update please run cleardb.py in the bot folder and launch the bot again")
            # we prepare our updater to continue after we die
            pull_updates(branch)
            await self.bot.close()
            #and kill the bot
            exit(0)
        else:
            await ctx.send("update cancled")

    @update.error
    async def update_error(self, ctx, error):

        if isinstance(error, MissingRequiredArgument):
            return await ctx.send(error)
        if isinstance(error, CommandInvokeError):
            if error.original.__class__.__name__ == "TimeoutError":
                await ctx.message.add_reaction("💤")
                await getattr(ctx, "reply").delete()
                return

    @command()
    @check(is_owner)
    async def purgedb(self, ctx):
        """Destroys the database."""
        await ctx.send("Removing the content and structure of the database...")
        clear_db()
        await ctx.send("Killing bot... Please reset to reinitialize DB")
        await self.bot.close()

        exit(1)

def setup(bot):
    if CONFIG.version_control.enable_update_cmd:
        # enable_update_cmd should only be used in the production and QA bots
        bot.add_cog(AutoUpdate(bot))
