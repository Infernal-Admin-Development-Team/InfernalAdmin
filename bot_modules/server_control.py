from discord.ext.commands import Cog


class ServerControl(Cog):
    """"General propose module for managing roles, spamming, bot permissions.etc"""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(ServerControl(bot))
