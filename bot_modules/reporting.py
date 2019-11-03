import discord
from discord.ext.commands import Cog, command

from database import *
from database.util import group_message_results


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

    async def print_report_to_server(self, report_id):
        """
        Checks if the report has its own channel, if not it creates one
        Will populate the channel with the initial report info
        """
        server = self.bot.get_guild(CONFIG.server)
        channel = None
        for c in server.channels:
            if c.id == CONFIG.reports_category:
                channel = await server.create_text_channel("report_" + str(report_id), category=c)
                break

    async def file_report(self, category, poster_id, offender_id, content, references):

        s = session()
        p = Report(poster_id=poster_id, offender_id=offender_id, content=content, category=category)
        s.add(p)
        s.flush()
        s.commit()
        s.close()


    @command()
    async def report(self, ctx):
        """->Submits a report to the admins"""
        reporter = ctx.message.author
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
                    while True:
                        msg = await self.bot.wait_for('message', timeout=120, check=check)
                        for m in guild.members:
                            if msg.content in m.name:
                                offender = m
                                break
                        if offender == None:
                            await ctx.message.author.send("No member found")
                        else:
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
                    report_content += msg.content

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
                        if results.count():
                            if results.count() > 1:
                                num_groups = 0
                                await ctx.message.author.send("I found multiple messages which match that content.")
                                result_groups = group_message_results(results)
                                for group in result_groups:
                                    author = await self.bot.fetch_user(group[0][0].author)
                                    channel = await self.bot.fetch_channel(group[0][0].channel)
                                    output = author.name + " at #" + channel.name + "```"
                                    for m in group:
                                        num_groups += 1
                                        result_canidates.append(m)
                                        output += "|" + str(num_groups) + "|  " + str(len(m)) + " instance(s) of " + m[
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
                                    if msg.content.isdigit() and 0 < int(msg.content) < len(result_canidates):
                                        for m in result_canidates[int(msg.content) - 1]:
                                            offending_msgs.append(m)
                                        break
                                    else:
                                        await ctx.message.author.send("Invalid choice")


                            elif results.count() == 0:
                                ctx.message.author.send("No results found")
                            else:
                                for r in results:
                                    offending_msgs.append(r)
                                await ctx.message.author.send(
                                    "Type 'done' or if you wish to add more messages copy them here")
                            await msg.add_reaction("✔")
                        else:
                            await msg.add_reaction("❌")
            await ctx.message.author.send("Please confirm")
            oname = "none"
            if offender != None:
                oname = offender.name
            report_msg = "**Offender**: " + offender.name + "\n"
            report_msg += "**Category**:" + self.category_list[selected_category] + "\n"
            report_msg += "```" + report_content + "```"
            report_msg += "**Evidence**:"
            await ctx.message.author.send(report_msg)
            for m in offending_msgs:
                await ctx.message.author.send("```" + m.content + "```")
            await ctx.message.author.send("Is this information correct? (y/n)")
            msg = await self.bot.wait_for('message', timeout=120, check=check)
            if 'y' in msg.content:
                break


        await ctx.message.author.send("sending report")

    """
    @report.error
    async def report_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(error)
        if isinstance(error, commands.CommandInvokeError):
            if error.original.__class__.__name__ == "TimeoutError":
                await ctx.message.add_reaction("💤")
                return
    """

def setup(bot):
    bot.add_cog(Reporting(bot))
