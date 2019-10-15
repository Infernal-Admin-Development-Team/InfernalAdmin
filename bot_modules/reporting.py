import discord
from discord.ext.commands import Cog, command


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


    @command()
    async def report(self, ctx):
        """->Submits a report to the admins"""
        reporter = ctx.message.author


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
        selected_category = msg.content

        await ctx.message.author.send("Was there an offender?(y/n)")
        msg = await self.bot.wait_for('message', timeout=120, check=check)
        offender_id = 0
        if 'y' in msg.content:
            await ctx.message.author.send("Please copy their name")
            msg = await self.bot.wait_for('message', timeout=120, check=check)

        await ctx.message.author.send("Please describe the issue.\n"
                                      "You can use as many messages as you need\n"
                                      "You can post screenshots here, but try not to.\n"
                                      "You will be able to paste messages for evidence in the next step\n"
                                      "say \"done\" when you are done")
        report_text = ""
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
