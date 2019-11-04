from discord.ext.commands import Cog, command

from InfernalAdmin.report_generator import ReportGenerator


class ReportViewing(Cog):
    """"Module which allows admins to view and manage reports. It also allows users to view the status of reports
    they submitted """

    def __init__(self, bot):
        self.bot = bot
        self.reportGen = ReportGenerator(self.bot)

    @command()
    async def view(self, ctx, report_id: int):
        await self.reportGen.print_report_to_server(report_id)

    """
    @view.error
    async def view_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(error)
        elif isinstance(error, commands.BadArgument):
            return await ctx.send(error)
        else:
            raise error
    """


def setup(bot):
    bot.add_cog(ReportViewing(bot))
