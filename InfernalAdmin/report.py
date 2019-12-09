import discord

import database as db
import database.msgutil as msgutil
import database.util as dbutil
from util import CONFIG, report_status_to_str, report_type_to_str


class Report:
    """Report class, used as an interface between discord and the report entries in the database"""

    def __init__(self, bot, report_id):
        self.bot = bot
        self.report_id = report_id
        s = db.session()
        self.report = s.query(db.Report).filter(db.Report.id == report_id).first()

        s.close()

    async def notify_user_of_comment(self):
        poster = await self.bot.fetch_user(self.report.poster_id)
        print(poster.name)
        await poster.send("A comment has been made on your report. Use " + CONFIG.prefix + "view " + str(
            self.report_id) + " to see the changes")

    def change_status(self, status):
        pass

    def get_references(self):
        if self.report:
            s = db.session()
            references = s.query(db.Message).join(db.Reference).filter(db.Reference.report_id == self.report_id)
            s.close()
            return references
        else:
            return None

    async def render(self, ctx, padding, show_all=False):
        if self.report:
            """Draws report to channel"""
            poster = self.bot.get_member(self.report.poster_id)

            e = discord.Embed(title="**Report# **" + str(self.report.id), colour=0xFF0000, type="rich")

            if poster == None:
                e.add_field(name="**POSTER:**", value=(await self.bot.fetch_user(self.report.poster_id)).name)
            else:
                e.add_field(name="**POSTER:**", value=poster.display_name)

            e.add_field(name="**STATUS:**", value='[' + report_status_to_str(self.report.status) + ']')
            e.add_field(name="**CATEGORY:**", value=report_type_to_str(int(self.report.category)))
            if self.report.offender_id != 0:
                offender = self.bot.get_member(self.report.offender_id)
                if offender == None:
                    e.add_field(name="**OFFENDER:**", value=(await self.bot.fetch_user(self.report.offender_id)).name)
                else:
                    e.add_field(name="**OFFENDER:**", value=offender.display_name)

            if len(self.report.content) > 1500:
                await ctx.send(embed=e)
                await ctx.send("**CONTENT**")
                await msgutil.send_long_msg(self.report.content, ctx)
            else:
                e.add_field(name="**CONTENT**", value=self.report.content)
                await ctx.send(embed=e)

            grouped_refrences = dbutil.group_message_results(self.get_references())
            for g in grouped_refrences:
                await msgutil.print_message_groups(g, ctx, self.bot, padding=10)

            s = db.session()
            comments = s.query(db.ReportComment).filter(db.ReportComment.report_id == self.report_id)
            if comments.count():
                await ctx.send("***COMMENTS***")
            for c in comments:
                if show_all:
                    print("showing all")
                    msg_to_send = s.query(db.Message).filter(db.Message.id == c.message_id).first()
                    if msg_to_send:
                        author = await self.bot.fetch_user(msg_to_send.author)
                        if c.visible_to_poster:
                            if author.id != self.report.poster_id:
                                await ctx.send("**" + author.name + "(to poster)**: " + msg_to_send.content)
                        else:
                            await ctx.send("**" + author.name + "**: " + msg_to_send.content)

                else:
                    if c.visible_to_poster:
                        msg_to_send = s.query(db.Message).filter(db.Message.id == c.message_id).first()
                        author = await self.bot.fetch_user(msg_to_send.author)
                        if author.id == self.report.poster_id:
                            await ctx.send("**You:**:" + msg_to_send.content)
                        else:
                            await ctx.send("**Admins:**:" + msg_to_send.content)
            await ctx.send("**END OF REPORT**")
            if show_all:
                await ctx.send("```anything said in this channel will be recorded as a comment on this report.\n"
                               "Say $comment to submit a message to the poster.\n"
                               "Say $resolve to mark this report as resolved\n"
                               "say $reject to mark this report as rejected```")
            s.close()

    async def get_report_channel(self):
        server = self.bot.get_guild(CONFIG.server)
        for c in server.channels:
            if c.id == self.report.channel:
                return c
        return None

    async def render_to_server(self):
        """
        Checks if the report has its own channel, if not it creates one
        Will populate the channel with the initial report info
        will return channel ID on success 0 otherwise. Will also open a session with the reportMgr
        """
        server = self.bot.get_guild(CONFIG.server)

        s = db.session()

        report = s.query(db.Report).filter(db.Report.id == self.report.id).first()



        if not report:
            return 0

        channel = None
        report_has_channel = False
        if report.channel:
            for c in server.channels:
                if c.id == self.report.channel:
                    channel = c
                    report_has_channel = True

        if not report_has_channel:
            for c in server.channels:
                if c.id == CONFIG.reports_category:
                    channel = await server.create_text_channel("report_" + str(self.report_id), category=c)
                    report.channel = channel.id
                    print("changing report(" + str(report.id) + ") channel to " + str(channel.id))
                    s.commit()
                    print(report.channel)
                    s.flush()
                    break
        s.close()
        if not report_has_channel:
            await self.render(channel, 10, show_all=True)

        return channel.id

    async def publish(self):
        """Will print the report to the server and notify all admins of the new report"""
        return await self.render_to_server()
