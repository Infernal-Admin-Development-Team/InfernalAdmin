import asyncio

import discord
from discord.ext.commands import Cog, command, check, group

from InfernalAdmin.report_generator import ReportGenerator
from util import *


class ReportViewing(Cog):
    """"Module which allows admins to view and manage reports. It also allows users to view the status of reports
    they submitted """

    def __init__(self, bot):
        self.bot = bot
        self.reportGen = ReportGenerator(self.bot)

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
            poster_name = "Invalid"
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
        if isinstance(ctx.message.channel, discord.DMChannel):
            s = db.session()
            report = s.query(db.Report).filter(db.Report.id == report_id).first()
            s.close()
            if report.poster_id == ctx.message.author.id:
                await self.reportGen.print_report(report_id, ctx, 5)
        else:
            if can_view_reports(ctx):
                if await self.check_if_in_main(ctx):
                    await ctx.message.delete()
                    channel_id = (await self.reportGen.print_report_to_server(report_id))
                    msg = await ctx.send(get_link_to_channel(channel_id))
                    await asyncio.sleep(10)
                    await msg.delete()

    """
    @view.error
    async def view_error(self, ctx, error):

        if isinstance(error, discord.ext.commands.MissingRequiredArgument):
            return await ctx.send(error)
        elif isinstance(error, discord.ext.commands.BadArgument):
            return await ctx.send(error)
        else:
            raise error
    """
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
            results = s.query(db.Report).filter(db.Report.poster_id == ctx.message.mentions[0].id)

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
                    if c.id == r.channel:
                        await c.delete()
                        break






def setup(bot):
    bot.add_cog(ReportViewing(bot))
