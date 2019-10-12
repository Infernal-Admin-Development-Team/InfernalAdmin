from discord.ext import commands
from pathlib import Path
import os
from github import Github
from subprocess import check_call as run
class AutoUpdate(commands.Cog):
    """This will contain everything relating to welcome"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def branches(self,ctx):
        """updates the bot"""
        #print("aaa")
        g=Github()
        repo = g.get_repo(self.bot.config['version-control']['repo'])
        branches=list(repo.get_branches())
        cwd = Path(os.getcwd())
        out_str=" "
        for b in branches:
            out_str+=b.name+"\n "
        await ctx.send("There are "+str(len(branches))+" branches\n```"+out_str+"```")

    @commands.command()
    async def update(self,ctx,branch:str):
        try:
            await ctx.send("Updating to ``"+branch+"``")
        except commands.errors.MissingRequiredArgument:
            await ctx.send("Invalid arguements")


