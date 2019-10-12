from discord.ext import commands
from pathlib import Path
import os
from github import Github

class AutoUpdate(commands.Cog):
    """This will contain everything relating to welcome"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def update(self,ctx):
        """updates the bot"""
        #print("aaa")
        g=Github()
        repo = g.get_repo(self.bot.config['version-control']['repo'])
        branches=list(repo.get_branches())
        cwd = Path(os.getcwd())

        await ctx.send(str(branches))

