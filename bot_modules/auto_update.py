import os
import shutil
import sys
from pathlib import Path

from discord.ext import commands
from discord.ext.commands import Cog, command, check
from github import Github

from util import *


def pull_and_reset(branch):
    cwd = Path(os.getcwd())
    parent = cwd.parent
    print("Resetting")
    """
    print("Resetting")
    cmd= "sleep 5; " \
         "git fetch --all; " \
        "git reset --hard origin/"+branch+"; "\
        "sleep(5); " \
        "python main.py;"
    with open("update.ps1","w+") as f:
        f.write(cmd)
    f.close()
    """
    shutil.copy2(os.getcwd() + "\\update_windows.py", parent + "\\update_windows.py")
    # subprocess.Popen(['C:\\Windows\\SysWOW64\\WindowsPowerShell\\v1.0\\powershell.exe', "./update.ps1"], shell=True)
    print("done")


    #



class AutoUpdate(Cog):
    """The AutoUpdate module contains everything needed to perform git operations on the bot
    it allows you to change the branch the bot is running on (to allow for easy testing of different branches)
    it also contains the check_for_updates task which is used in the production bot
    """

    def __init__(self, bot):

        self.bot = bot

    def get_branch_names(self):
        g = Github()
        repo = g.get_repo(CONFIG.version_control.repo)
        ret_list =[]
        for b in repo.get_branches():
            ret_list.append(b.name)
        return ret_list

    @command()
    async def branches(self,ctx):
        """->Gets the branches from the github repo"""
        out_str=" "
        branches=self.get_branch_names()

        for b in branches:
            out_str+=b+"\n "
        await ctx.send("There are "+str(len(branches))+" branches\n```"+out_str+"```")


    @commands.command()
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
            await ctx.send("Updating to ``" + branch + "``")

            pull_and_reset(branch)
            await self.bot.close()
            sys.exit()
        else:
            await ctx.send("update cancled")

    @update.error
    async def update_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(error)
        if isinstance(error, commands.CommandInvokeError):
            if error.original.__class__.__name__ == "TimeoutError":
                await ctx.message.add_reaction("💤")
                await getattr(ctx, "reply").delete()
                return

def setup(bot):
    bot.add_cog(AutoUpdate(bot))

