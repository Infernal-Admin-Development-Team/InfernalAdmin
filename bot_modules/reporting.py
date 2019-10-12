from discord.ext.commands import Cog, command


class Reporting(Cog):
    """The AutoUpdate module contains everything needed to perform git operations on the bot"""

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def report(self, ctx):
        """Submits a report to the admins"""
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Reporting(bot))
