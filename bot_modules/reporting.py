import discord
from discord.ext import commands
from discord.ext.commands import Cog, command

import database.msgutil as msgutil
import database.util as dbutil
from InfernalAdmin.report_generator import ReportGenerator
from database import *


class Reporting(Cog):
    """The reporting Module allows users to submit reports to the admins."""

    def __init__(self, bot):
        self.bot = bot
        self.category_list = ["admin abuse",
                              "dispute between users",
                              "spam",
                              "bot abuse",
                              "harrasssment",
                              "server issue"]
        self.active_report_sessions = []
        self.report_gen = ReportGenerator(self.bot)

    @command()
    async def report(self, ctx):
        """->Submits a report to the admins"""
        reporter = ctx.message.author
        if reporter in self.active_report_sessions:
            return
        self.active_report_sessions.append(reporter)
        server = self.bot.get_guild(CONFIG.server)

        guild = self.bot.get_guild(CONFIG.server)

        def check(m):
            if isinstance(m.channel, discord.DMChannel):
                return m.author == reporter


        if not isinstance(ctx.message.channel, discord.DMChannel):
            await ctx.message.delete()
        while True:
            offender = None
            selected_category = None
            report_text = ""
            member_name = ""
            dm = await ctx.message.author.send(
                "Please select one of the following categories.\n"
                "```Admin Abuse\n"
                "Dispute between users\n"
                "Spam\n"
                "Bot abuse\n"
                "Harrasssment\n"
                "Server Issue```")

            msg = await self.bot.wait_for('message', timeout=120, check=check)
            while msg.content.lower() not in self.category_list:
                await ctx.message.author.send("Invalid category please try again.")
                msg = await self.bot.wait_for('message', timeout=120, check=check)

            selected_category = self.category_list.index(msg.content.lower())

            await ctx.message.author.send("Was there an offender?(y/n)")
            while True:
                msg = await self.bot.wait_for('message', timeout=120, check=check)
                if 'y' in msg.content:
                    await ctx.message.author.send("Please copy their name.")
                    count = 0
                    membernames = []
                    while True:
                        msg = await self.bot.wait_for('message', timeout=120, check=check)
                        for m in guild.members:

                            nick = ""
                            if m.nick:
                                nick = m.nick
                            if msg.content in m.name or msg.content in nick:
                                offender = m
                                count += 1
                                membernames.append([m.name, nick])

                        if offender == None:
                            await ctx.message.author.send("No member found")
                        elif count > 1:
                            await ctx.message.author.send("Multiple members found")
                            for names in membernames:
                                await ctx.message.author.send(names[0] + ", nickname: " + names[1])
                            await ctx.message.author.send("Please copy one of the users above")
                            count = 0
                            membernames = []
                            offender = None
                        else:
                            if offender.nick:
                                await ctx.message.author.send("Using user:" + offender.name + ", nick:" + offender.nick)
                            else:
                                await ctx.message.author.send("Using user:" + offender.name)
                            break
                elif 'n' in msg.content:
                    break
                else:
                    await ctx.message.author.send("Please say yes or no")
                if offender != None:
                    break

            await ctx.message.author.send("Please describe the issue.\n"
                                          "You can use as many messages as you need\n"
                                          "You can post screenshots here, but try not to.\n"
                                          "You will be able to paste messages for evidence in the next step\n"
                                          "say \"done\" when you are done")
            report_content = ""
            while True:
                msg = await self.bot.wait_for('message', timeout=120, check=check)
                if msg.content == "done":
                    break
                else:
                    report_content += msg.content + "\n"

            await ctx.message.author.send("Please copy any relevant messages from the offender.\n"
                                          "If there were no offending messages please say \"done\""
                                          "If the messages were deleted, just paste any messages that occured on"
                                          "the same channel above or below the offending messages"
                                          "say \"done\" when you are done")

            offending_msgs = []
            if offender != None:

                while True:
                    msg = await self.bot.wait_for('message', timeout=120, check=check)
                    if msg.content == "done":
                        break
                    else:
                        s = session()
                        results = s.query(Message).filter(Message.content.ilike("%" + msg.content + "%"))
                        result_canidates = []

                        s.close()
                        if results.count():
                            if results.count() > 1:
                                num_groups = 0

                                result_groups = dbutil.group_message_results(results)
                                if len(result_groups) == 1:
                                    for m in result_groups[0]:
                                        offending_msgs.append(m)

                                else:
                                    await ctx.message.author.send("I found multiple messages which match that content.")
                                    for group in result_groups:
                                        author = await self.bot.fetch_user(group[0][0].author)
                                        channel = await self.bot.fetch_channel(group[0][0].channel)
                                        output = author.name + " at #" + channel.name + "```"
                                        for m in group:
                                            num_groups += 1
                                            result_canidates.append(m)
                                            output += "|" + str(num_groups) + "|  " + str(len(m)) + " instance(s) of " + \
                                                      m[
                                                          0].content[
                                                      :75] + " at " + str(
                                                m[0].timestamp) + "\n"
                                        output += "```"
                                        await ctx.message.author.send(output)
                                    await ctx.message.author.send(
                                        "Please select the number that corresponds to the instance")
                                    while True:
                                        print(len(result_canidates), num_groups)
                                        msg = await self.bot.wait_for('message', timeout=120, check=check)
                                        if msg.content.isdigit() and 0 < int(msg.content) <= len(result_canidates):

                                            offending_msgs.append(result_canidates[int(msg.content) - 1])

                                            break
                                        else:
                                            await ctx.message.author.send("Invalid choice")


                            elif results.count() == 0:
                                ctx.message.author.send("No results found")
                            else:
                                for r in results:
                                    offending_msgs.append([r])
                                await ctx.message.author.send(
                                    "Type 'done' or if you wish to add more messages copy them here")
                            await msg.add_reaction("✔")
                        else:
                            await ctx.message.author.send("Could not find message in server")
            await ctx.message.author.send("Please confirm")

            report_msg = ""
            if offender != None:
                report_msg += "**Offender**: " + offender.name + "\n"

            report_msg += "**Category**:" + self.category_list[selected_category] + "\n"
            if len(report_content):
                report_msg += "```" + report_content + "```"
            report_msg += "**Evidence**:"

            await ctx.message.author.send(report_msg)
            await msgutil.print_message_groups(offending_msgs, ctx.message.author, self.bot, padding=3)
            await ctx.message.author.send("Is this information correct? (y/n)")
            msg = await self.bot.wait_for('message', timeout=120, check=check)
            if 'y' in msg.content:
                break


        await ctx.message.author.send("sending report")
        report_id = 0
        if offender == None:
            report_id = dbutil.add_report(selected_category, ctx.message.author.id, 0, report_content, msg.created_at,
                                          [])
        else:
            final_msg_id_list = []
            final_offending_msg_list = []
            for g in offending_msgs:
                for m in g:
                    if m.id not in final_msg_id_list:
                        final_offending_msg_list.append(m)
                        final_msg_id_list.append(m.id)

            report_id = dbutil.add_report(selected_category, ctx.message.author.id, offender.id, report_content,
                                          msg.created_at, final_offending_msg_list)
        await ctx.message.author.send("Your report ``" + str(report_id) + "`` Has been submitted!")
        await ctx.message.author.send(
            "You can use ``" + CONFIG.prefix + "view " + str(report_id) + "`` to view the status of the report")
        await ctx.message.author.send(
            "You can use ``" + CONFIG.prefix + "myreports`` to view all the reports you have submitted")
        self.active_report_sessions.remove(ctx.message.author)
        await self.report_gen.print_report_to_server(report_id)

    @report.error
    async def report_error(self, ctx, error):
        self.active_report_sessions.remove(ctx.message.author)
        if isinstance(error, commands.CommandInvokeError):
            if error.original.__class__.__name__ == "TimeoutError":
                await ctx.message.author.send(
                    "Your session has expired due to inactivity. Please run ``" + CONFIG.prefix + "report`` again if you wish to continue")
        else:
            raise error
    

def setup(bot):
    bot.add_cog(Reporting(bot))
