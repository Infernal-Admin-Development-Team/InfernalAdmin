import discord
from discord.ext.commands import Cog, command

from database import *


class Reporting(Cog):
    """The reporting Module allows users to submit reports to the admins."""

    def __init__(self, bot):
        self.bot = bot
        self.catagory_list = ["admin abuse",
                              "dispute between users",
                              "spam",
                              "bot abuse",
                              "harrasssment",
                              "server issue"]

    async def file_report(self, category, poster_id, offender_id, content, references):
        server = self.bot.get_guild(CONFIG.server)
        s = session()
        p = Report(poster_id=poster_id, offender_id=offender_id, content=content, category=category)
        # s.add(p)
        # s.commit()
        s.close()
        for c in server.channels:
            print(c.name)
            if c.id == CONFIG.reports_category:
                await server.create_text_channel("test", category=c)

    @command()
    async def report(self, ctx):
        """->Submits a report to the admins"""
        reporter = ctx.message.author
        server = self.bot.get_guild(CONFIG.server)
        offender = None
        selected_category = None
        report_text = ""
        member_name = ""

        def check(m):
            if isinstance(m.channel, discord.DMChannel):
                return m.author == reporter


        if not isinstance(ctx.message.channel, discord.DMChannel):
            await ctx.message.delete()
        dm = await ctx.message.author.send(
            "Please select one of the following categories.\n"
            "```Admin Abuse\n"
            "Dispute between users\n"
            "Spam\n"
            "Bot abuse\n"
            "Harrasssment\n"
            "Server Issue```")

        msg = await self.bot.wait_for('message', timeout=120, check=check)
        while msg.content.lower() not in self.catagory_list:
            await ctx.message.author.send("Invalid category please try again.")
            msg = await self.bot.wait_for('message', timeout=120, check=check)

        selected_category = self.catagory_list.index(msg.content.lower())

        await ctx.message.author.send("Was there an offender?(y/n)")
        msg = await self.bot.wait_for('message', timeout=120, check=check)

        if 'y' in msg.content:
            await ctx.message.author.send("Please copy their name")
            while True:
                msg = await self.bot.wait_for('message', timeout=120, check=check)


        await ctx.message.author.send("Please describe the issue.\n"
                                      "You can use as many messages as you need\n"
                                      "You can post screenshots here, but try not to.\n"
                                      "You will be able to paste messages for evidence in the next step\n"
                                      "say \"done\" when you are done")

        while True:
            msg = await self.bot.wait_for('message', timeout=120, check=check)
            if msg.content == "done":
                break
            else:
                report_text += msg.content + "\n"

        await ctx.message.author.send("sending report")
        await ctx.message.author.send("Your report ```" + report_text + "```")










def setup(bot):
    bot.add_cog(Reporting(bot))
