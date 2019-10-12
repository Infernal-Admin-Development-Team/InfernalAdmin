from discord.ext.commands import Cog,command,check
from discord.ext import commands
from pathlib import Path
from subprocess import check_call as run
import os
import sys
from github import Github
from subprocess import check_call as run
from util import *
import subprocess

def pull_and_reset(branch):
    print("Resetting")
    run("git init; git remote add origin https://github.com/PeterGibbs/InfernalAdmin.git; (git fetch --all); git reset --hard origin/"+branch+"; sleep(15); echo Finished")


    print("done")
    sys.exit()
    #



class AutoUpdate(Cog):
    """The AutoUpdate module contains everything needed to perform git operations on the bot"""

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
    async def updateTest(self,ctx):
        await ctx.send("aaa")

    @command(hidden=True)
    async def branches(self,ctx):
        """updates the bot"""
        #print("aaa")


        out_str=" "
        branches=self.get_branch_names()

        for b in branches:
            out_str+=b+"\n "
        await ctx.send("There are "+str(len(branches))+" branches\n```"+out_str+"```")




    @commands.command()
    @check(is_owner)
    async def update(self, ctx, branch: str):
        """Causes the bot to update its local files to match the branch of your choosing"""

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
        else:
            await ctx.send("update cancled")

    @update.error
    async def update_error(self, ctx, error):

        # if ctx.command==self.update:
        #   return await ctx.send("update error"+error)

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(error)
        if isinstance(error, commands.CommandInvokeError):
            if error.original.__class__.__name__ == "TimeoutError":
                await ctx.message.add_reaction("💤")
                await getattr(ctx, "reply").delete()
                return

def setup(bot):
    bot.add_cog(AutoUpdate(bot))

