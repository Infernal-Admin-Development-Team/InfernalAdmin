from discord.ext.commands import Cog, command, check

from database import clear_db
from util import *


class ServerControl(Cog):
    """"General propose module for managing roles, spamming, bot permissions.etc"""

    def __init__(self, bot):
        self.bot = bot

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
    bot.add_cog(ServerControl(bot))

