import asyncio

from discord.ext import commands
from discord.ext.commands import Cog, command, check

from InfernalAdmin.report import Report
from util import *


def in_report_channel(ctx):
    """Used to ensure the report interaction commands are actually used in the right channels"""
    if isinstance(ctx.channel, discord.DMChannel):
        return False

    s = db.session()

    count = s.query(db.Report).filter(db.Report.channel == ctx.channel.id).count()
    s.close()
    return count > 0


def get_report_from_channel(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        return None

    s = db.session()
    report = s.query(db.Report).filter(db.Report.channel == ctx.channel.id).first()
    s.close()
    return report


class ReportInteraction(Cog):
    """Module used to allow admins to interact with reports
    Such interactions include setting status of reports,
    commenting on reports, and sending updates on the reports to the poster"""

    def __init__(self, bot):
        self.bot = bot

    @command()
    @check(can_resolve_reports)
    @check(in_report_channel)
    async def resolve(self, ctx):
        """->Sets the status of the report to Resolved"""
        report = get_report_from_channel(ctx)

    @command()
    @check(can_resolve_reports)
    @check(in_report_channel)
    async def reject(self, ctx):
        """->Sets the status of the report to Rejected"""
        report = get_report_from_channel(ctx)

    @command()
    @check(can_resolve_reports)
    @check(in_report_channel)
    async def progress(self, ctx):
        """->Sets the status of the report to IN PROGRESS"""
        report = get_report_from_channel(ctx)

    @command()
    @check(can_comment_reports)
    @check(in_report_channel)
    async def comment(self, ctx):
        """Posts a comment on the report thread, can be used for notes, will be saved
                even if the channel is deleted or clearreports is run"""
        msg0 = ctx.message
        def check(m):
            return m.channel == ctx.message.channel

        poster_id = 0
        report_id = 0
        msg1 = await ctx.send("The next message you send will be forwarded to the submitter of the report")
        msg2 = await self.bot.wait_for('message', timeout=120, check=check)
        print("reply posted")
        await asyncio.sleep(5)  # wait for message to be added to DB

        print("done waiting")
        s = db.session()
        comment = s.query(db.Message).filter(db.Message.msg_id == msg2.id).first()
        report_comment = s.query(db.ReportComment).filter(db.ReportComment.message_id == comment.id).first()
        report_comment.visible_to_poster = True
        report_id = report_comment.report_id
        s.commit()
        s.close()

        report = Report(self.bot, report_id)
        await report.notify_user_of_comment()

        await ctx.send("**" + msg0.author.name + "(to report poster)**: " + msg2.content)
        await msg0.delete()
        await msg1.delete()
        await msg2.delete()

    @comment.error
    async def comment_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if error.original.__class__.__name__ == "TimeoutError":
                msg = await ctx.send(
                    "Your session has expired due to inactivity. Please run ``" + CONFIG.prefix + "report`` again if you wish to continue")
                await asyncio.sleep(10)
                await msg.delete()
        else:
            raise error

def setup(bot):
    bot.add_cog(ReportInteraction(bot))
