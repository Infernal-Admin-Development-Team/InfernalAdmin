from discord.ext.commands import Cog


class Analytics(Cog):
    """"Soon to be analytics module"""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Analytics(bot))
