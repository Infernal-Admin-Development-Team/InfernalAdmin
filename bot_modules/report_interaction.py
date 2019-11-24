from discord.ext.commands import Cog


class ReportInteraction(Cog):
    """Module used to allow admins to interact with reports
    Such interactions include setting status of reports,
    commenting on reports, and sending updates on the reports to the poster"""

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(ReportInteraction(bot))
