from discord.ext import commands
from discord.ext.commands import Cog


class ServerControl(Cog):
    """"General propose module for managing roles, spamming, bot permissions.etc"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def mike(self, ctx):
        myid = '<@229379462968508417>'
        await ctx.send(myid + ' I already have a welcome function, you should add the picture code')
def setup(bot):
    bot.add_cog(ServerControl(bot))
