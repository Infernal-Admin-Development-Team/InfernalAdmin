import discord
from discord.ext.commands import Cog, command, check

from InfernalAdmin.report_generator import ReportGenerator
from util import *


class ReportViewing(Cog):
    """"Module which allows admins to view and manage reports. It also allows users to view the status of reports
    they submitted """

    def __init__(self, bot):
        self.bot = bot
        self.reportGen = ReportGenerator(self.bot)

    async def send_list(self, ctx, results):
        str_out = "```"
        count = 0
        for r in results:
            count += 1
            content = r.content[:20] + (r.content[20:] and '...')
            if content[-1] == "\n":
                content = content[:-1]
            str_out += "ID: " + str(r.id) + " Type: " + report_type_to_str(
                int(r.category)) + " Status: " + report_status_to_str(int(r.status)) + " Desc: " + content + "\n"
        if count > 0:
            str_out += "```"
            await ctx.send("I found " + str(count) + " Reports")
            await ctx.send(str_out)
            await ctx.send("Use " + CONFIG.prefix + "view <ID> to see more info on a report")



    @command()
    async def view(self, ctx, report_id: int):
        if isinstance(ctx.message.channel, discord.DMChannel):
            s = db.session()
            report = s.query(db.Report).filter(db.Report.id == report_id).first()
            s.close()
            if report.poster_id == ctx.message.author.id:
                await self.reportGen.print_report(report_id, ctx, 5)
        else:
            if can_view_reports(ctx):
                await self.reportGen.print_report_to_server(report_id)

    @command()
    async def myreports(self, ctx):
        if not isinstance(ctx.message.channel, discord.DMChannel):
            await ctx.message.delete()
        ctx = ctx.message.author

        s = db.session()
        results = s.query(db.Report).filter(db.Report.poster_id == ctx.id)
        s.close()
        await self.send_list(ctx, results)

    @command()
    @check(can_view_reports)
    async def listreports(self, ctx):
        if isinstance(ctx.message.channel, discord.DMChannel):
            await ctx.message.author.send("Please use " + get_link_to_channel(CONFIG.reports_channel))
        else:
            print(ctx.message.channel.id)
            if ctx.message.channel.id != CONFIG.reports_channel:
                await ctx.message.delete()
                await ctx.message.author.send("Please use " + get_link_to_channel(CONFIG.reports_channel))
            else:
                s = db.session()
                results = s.query(db.Report)
                s.close()
                await self.send_list(ctx, results)
        # s = db.session()
        # reports = s.query(db.Report).filter(db.Report.poster_id == ctx.id)
        # s.close()

    @command()
    @check(can_view_reports)
    async def clearreports(self, ctx):
        """Clears the channels in the reports category"""
        server = self.bot.get_guild(CONFIG.server)
        s = db.session()
        results = s.query(db.Report)
        s.close()
        for r in results:

            if r.channel:
                for c in server.channels:
                    if c.id == r.channel:
                        await c.delete()
                        break



    @view.error
    async def view_error(self, ctx, error):

        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            return await ctx.send(error)
        elif isinstance(error, discord.ext.commands.BadArgument):
            return await ctx.send(error)
        else:
            raise error


def setup(bot):
    bot.add_cog(ReportViewing(bot))
