import database as db
import database.msgutil as msgutil
import database.util as dbutil
from util import CONFIG, report_status_to_str, report_type_to_str


class ReportGenerator:
    def __init__(self, bot):
        self.bot = bot

    async def print_report(self, report_id, ctx, padding):
        s = db.session()
        report = s.query(db.Report).filter(db.Report.id == report_id).first()
        s.close()
        header = ""
        header += ("**REPORT-ID**    " + str(report.id) + "\n")
        header += ("**STATUS**          " + report_status_to_str(report.status) + "\n")
        header += ("**CATEGORY**    " + report_type_to_str(int(report.category)) + "\n")
        header += ("**POSTER**           " + (await self.bot.fetch_user(report.poster_id)).name + "\n")
        if report.offender_id != 0:
            header += ("**OFFENDER**      " + (await self.bot.fetch_user(report.offender_id)).name + "\n")
        else:
            header += "**OFFENDER**      NONE\n"
        header += "**CONTENT** "
        await ctx.send(header)
        await msgutil.send_long_msg(report.content, ctx)
        refrences = s.query(db.Message).join(db.Reference).filter(db.Reference.report_id == report_id)
        grouped_refrences = dbutil.group_message_results(refrences)
        for g in grouped_refrences:
            await msgutil.print_message_groups(g, ctx, self.bot, padding=10)

    async def print_report_to_server(self, report_id):
        """
        Checks if the report has its own channel, if not it creates one
        Will populate the channel with the initial report info
        will return channel ID on success 0 otherwise
        """
        server = self.bot.get_guild(CONFIG.server)

        s = db.session()

        report = s.query(db.Report).filter(db.Report.id == report_id).first()

        if not report:
            return 0

        channel = None
        report_has_channel = False
        if report.channel:
            for c in server.channels:
                if c.id == report.channel:
                    channel = c
                    report_has_channel = True

        if report_has_channel == False:
            for c in server.channels:
                if c.id == CONFIG.reports_category:
                    channel = await server.create_text_channel("report_" + str(report_id), category=c)
                    report.channel = channel.id
                    s.commit()
                    s.flush()
                    break
        s.close()
        if report_has_channel == False:
            await self.print_report(report_id, channel, 10)
        return channel.id

    async def publish_new_report(self, report_id):
        """Will print the report to the server and notify all admins of the new report"""
        await self.print_report_to_server(report_id)
