import asyncio

from discord.ext.commands import Cog, command, check, group

from InfernalAdmin.report import Report
from util import *


class ReportViewing(Cog):
    """"Module which allows admins to view and manage reports. It also allows users to view the status of reports
    they submitted """

    def __init__(self, bot):
        self.bot = bot


    async def check_if_in_main(self, ctx):
        if isinstance(ctx.message.channel, discord.DMChannel):
            await ctx.message.author.send(
                "Please use " + get_link_to_channel(CONFIG.reports_channel) + " When querying reports")
            return False
        else:
            print(ctx.message.channel.id)
            if ctx.message.channel.id != CONFIG.reports_channel:
                await ctx.message.delete()
                await ctx.message.author.send(
                    "Please use " + get_link_to_channel(CONFIG.reports_channel) + " When querying reports")
                return False
            else:
                return True
    async def send_list(self, ctx, results):

        count = 0
        e = discord.Embed(colour=0x19D719, title="Results")


        for r in results:

            offender = None
            if r.offender_id:
                offender = self.bot.get_member(r.offender_id)
            poster = self.bot.get_member(r.poster_id)
            offender_name = "None"
            content = r.content[:40] + (r.content[40:] and '...')
            if not poster:
                poster_name = (await self.bot.fetch_user(r.poster_id)).name
            else:
                poster_name = poster.display_name

            if r.offender_id != 0:
                if offender:
                    offender_name = (await self.bot.fetch_user(r.offender_id)).name

            result_str = "**Status:** " + report_status_to_str(int(r.status)) + "\t"
            result_str += "**Category:** " + report_type_to_str(int(r.category)) + "\t"
            result_str += "**Poster:** " + poster_name + "\t"
            result_str += "**Offender:** " + offender_name + "\t"
            result_str += "**Timestamp:** " + str(r.timestamp) + "\n"
            result_str += "**Content:** " + content

            e.add_field(name="**Report-ID:** " + str(r.id), value=result_str, inline=False)
            count += 1
        e.set_footer(text=str(count) + ' record(s)')
        msg1 = (await ctx.send(embed=e))
        msg2 = (await ctx.send("Use " + CONFIG.prefix + "view <ID> to see more info on a report"))

        await asyncio.sleep(50)
        await msg1.delete()
        await msg2.delete()

    @command()
    async def view(self, ctx, report_id: int):
        rep = Report(self.bot, report_id)
        if not rep.report:
            msg = await ctx.send("Report not found")
            await asyncio.sleep(10)
            await msg.delete()
            return
        if isinstance(ctx.message.channel, discord.DMChannel):
            s = db.session()
            report = s.query(db.Report).filter(db.Report.id == report_id).first()
            reporter = rep.report.poster_id
            s.close()

            def check(m):
                if isinstance(m.channel, discord.DMChannel):
                    return m.author.id == reporter

            if report.poster_id == ctx.message.author.id:
                await rep.render(ctx, 5)

                while True:
                    await ctx.send(
                        "```to leave a comment on this report say 'comment'"
                        "say anything else to exit```")
                    msg = await self.bot.wait_for('message', timeout=120, check=check)
                    if msg.content.lower() == "comment":
                        await ctx.send(
                            "The next message you post will be saved in the report and will be visible to the admins")
                        msg2 = await self.bot.wait_for('message', timeout=120, check=check)

                        s = db.session()
                        message2add = db.Message(msg_id=msg2.id, channel=msg2.channel.id, author=msg2.author.id,
                                                 content=msg2.content, timestamp=msg2.created_at)
                        s.add(message2add)

                        s.flush()

                        attachments = []
                        for a in msg2.attachments:
                            att = db.Attachment(file_link=a.url, message_id=message2add.id)
                            attachments.append(att)
                        s.add_all(attachments)
                        s.commit()
                        s.flush()

                        rep_comment = db.ReportComment(message_id=message2add.id, report_id=rep.report.id,
                                                       visible_to_poster=True)
                        s.add(rep_comment)
                        s.commit()
                        s.close()
                        channel = await rep.get_report_channel()
                        print(channel)
                        if channel:
                            author = msg2.author.name
                            print(author)
                            await channel.send("***" + str(author) + "***: " + str(msg2.content))

                        else:

                            await rep.render_to_server()
                    else:
                        await ctx.send(
                            "Leaving interactive session")
                        return





        else:
            if can_view_reports(ctx):
                if await self.check_if_in_main(ctx):
                    await ctx.message.delete()
                    channel_id = await rep.render_to_server()
                    msg = await ctx.send(get_link_to_channel(channel_id))
                    await asyncio.sleep(10)
                    await msg.delete()

    @view.error
    async def view_error(self, ctx, error):

        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            return await ctx.send(error)
        elif isinstance(error, discord.ext.commands.BadArgument):
            return await ctx.send(error)
        elif isinstance(error, discord.ext.commands.CommandInvokeError):
            if error.original.__class__.__name__ == "TimeoutError":
                await ctx.message.author.send(
                    "Your session has expired due to inactivity. Please run ``" + CONFIG.prefix + "view`` again if you wish to continue")
        else:
            raise error

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
        if await self.check_if_in_main(ctx):

            print(ctx.message.channel.id)
            if ctx.message.channel.id != CONFIG.reports_channel:
                await ctx.message.delete()
                await ctx.message.author.send("Please use " + get_link_to_channel(CONFIG.reports_channel))
            else:
                msg1 = (await ctx.send("Grabbing list please wait.."))

                s = db.session()
                results = s.query(db.Report)
                s.close()
                await self.send_list(ctx, results)
                await msg1.delete()
                await ctx.message.delete()

    @check(can_view_reports)
    @group(invoke_without_command=True)
    async def search(self, ctx):
        """"search c <category> ->returns a list of reports matching the category
            search k <keyword> ->returns a list of reports with the keyword in the report description
            search r <mention> ->returns a list of reports in which the user entered filed
            search o <mention> ->returns a list of reports in which the user entered was the offender in"""
        msg = (await ctx.send("```search c <category> ->returns a list of reports matching the category\n"
                              "search k <keyword> ->returns a list of reports with the keyword in the report description\n"
                              "search r <mention> ->returns a list of reports in which the user entered filed\n"
                              "search o <mention> ->returns a list of reports in which the user entered was the offender in```"))

        await asyncio.sleep(20)
        await msg.delete()
        await ctx.message.delete()

    @search.command()
    async def c(self, ctx, k_word: str):

        """returns a list of reports matching the category"""
        category_list = ["admin abuse",
                         "dispute between users",
                         "spam",
                         "bot abuse",
                         "harassment",
                         "server issue"]
        index = 0
        valid_input = False
        for c in category_list:
            if ctx.message.content.lower() in c.lower() or c.lower() in ctx.message.content.lower():
                valid_input = True
                break
            index += 1
        if not valid_input:
            msg = await ctx.send(
                "Please select one of the following categories.\n"
                "```Admin Abuse\n"
                "Dispute between users\n"
                "Spam\n"
                "Bot abuse\n"
                "Harassment\n"
                "Server Issue```")
            await asyncio.sleep(10)
        else:
            msg = (await ctx.send("searching for all reports with Category: " + k_word))
            s = db.session()
            results = s.query(db.Report).filter(db.Report.category == str(index))
            s.close()
            await self.send_list(ctx, results)
        await msg.delete()
        await ctx.message.delete()

    @search.command()
    async def k(self, ctx, *, k_word):
        """returns a list of reports with the keyword in the report description"""

        msg = (await ctx.send("searching for all reports which contain **" + k_word + "** in their description.."))
        s = db.session()

        results = s.query(db.Report).filter(db.Report.content.ilike("%" + k_word + "%"))
        s.close()
        await self.send_list(ctx, results)
        await msg.delete()
        await ctx.message.delete()

    @search.command()
    async def r(self, ctx):
        """returns a list of reports in which the user entered filed"""
        members = []

        if len(ctx.message.mentions) == 0:
            msg = (await ctx.send("please provide a valid mention"))
            await asyncio.sleep(10)
        else:
            msg = (await ctx.send("searching for all reports submitted by: **" + ctx.message.mentions[0].name + "**"))
            s = db.session()
            results = s.query(db.Report).filter(db.Report.poster_id == ctx.message.mentions[0].id)

            s.close()
            await self.send_list(ctx, results)
        await msg.delete()
        await ctx.message.delete()

    @search.command()
    async def o(self, ctx, *, k_word):
        """returns a list of reports in which the user entered was the offender in"""
        if len(ctx.message.mentions) == 0:
            msg = (await ctx.send("please provide a valid mention"))
            await asyncio.sleep(10)
        else:
            msg = (await ctx.send(
                "searching for all reports in which **" + ctx.message.mentions[0].name + "** was the offender"))
            s = db.session()
            results = s.query(db.Report).filter(db.Report.offender_id == ctx.message.mentions[0].id)

            s.close()
            await self.send_list(ctx, results)
        await msg.delete()
        await ctx.message.delete()

    @search.error
    async def search_error(self, ctx, error):

        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            return await ctx.send(error)
        elif isinstance(error, discord.ext.commands.BadArgument):
            return await ctx.send(error)
        else:
            raise error
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
                    print("R:" + str(r.channel) + "   C:" + str(c.id))
                    if c.id == r.channel:
                        print("removing channel")
                        await c.delete()
                        break






def setup(bot):
    bot.add_cog(ReportViewing(bot))
