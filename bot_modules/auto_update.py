from discord.ext.commands import Cog,command,check
from discord.ext import commands
from pathlib import Path
import os
from github import Github
from subprocess import check_call as run
from util import *
class CogEx(Cog):
    def __init__(self,bot):
        super().__init__(bot)


class AutoUpdate(Cog):
    """The AutoUpdate module contains everything needed to perform git operations on the bot"""

    def __init__(self, bot):

        self.bot = bot





    @command(hidden=True)
    async def branches(self,ctx):
        """updates the bot"""
        #print("aaa")
        g=Github()
        repo = g.get_repo(self.bot.config.version_control.repo)
        branches=list(repo.get_branches())
        cwd = Path(os.getcwd())
        out_str=" "
        for b in branches:
            out_str+=b.name+"\n "
        await ctx.send("There are "+str(len(branches))+" branches\n```"+out_str+"```")





    @command(hidden=True)
    @check(is_owner)
    async def update(self,ctx,branch:str):
            """Causes the bot to update its local files to match the branch of your choosing"""
            
            def check(m):
                return m.author==ctx.message.author and m.channel==ctx.message.channel

            await ctx.send("Are you sure you want to update the bot to ``" + branch + "``")

            msg= await self.bot.wait_for('message',timeout=5, check=check)
            if "y" in msg.content:
                await ctx.send("Updating to ``"+branch+"``")
            else:
                await ctx.send("update cancled")


    async def cog_command_error(self, ctx, error):


        #if ctx.command==self.update:
        #   return await ctx.send("update error"+error)

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(error)
        if isinstance(error,commands.CommandInvokeError):
            if error.original.__class__.__name__ == "TimeoutError":
                return await ctx.message.rea("GB")
            #return await ctx.send(error.original)
        #return await ctx.send(str(error.original))
        #if str(error.origional)=="TimeoutError":
        #    return await ctx.send(":clock1:")

def setup(bot):
    bot.add_cog(AutoUpdate(bot))

