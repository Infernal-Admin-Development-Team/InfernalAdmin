from discord.ext.commands import Cog, command, check

from util import *


class Analytics(Cog):
    """"Soon to be analytics module"""

    def __init__(self, bot):
        self.bot = bot

    @command()
    @check(is_owner)
    async def getoldusers(self, ctx):
        """As of right now it only gets users who did not post on the server since the bot went online"""
        s = db.session()

        for member in self.bot.get_guild(CONFIG.server).members:

            message = s.query(db.Message).filter(db.Message.author == member.id).first()
            if not message:
                await ctx.send("No messages from " + member.name)

        s.close()

def setup(bot):
    bot.add_cog(Analytics(bot))
