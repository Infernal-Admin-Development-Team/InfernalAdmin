from discord.ext.commands import Cog, command

from util import CONFIG


class Testing(Cog):
    """Small module used to create admin roles, and allow you to change your role to them
    NOT TO BE ENABLED IN THE PRODUCTION BOT.
    """

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def mkrole(self, ctx):
        print("aaa")


def setup(bot):
    if CONFIG.enable_testing:
        # enable_update_cmd should only be used in the production and QA bots
        bot.add_cog(Testing(bot))
