from discord.ext.commands import Cog, command


class CauseError(Cog):
    """Kills the bot to test the error handling
    """

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def crash(self, ctx):
        """Throws an error to """
        await ctx.send("Creating error")


def setup(bot):
    bot.add_cog(CauseError(bot))
