import discord
from discord.ext.commands import Cog, command


class Reporting(Cog):
    """The AutoUpdate module contains everything needed to perform git operations on the bot"""

    def __init__(self, bot):
        self.bot = bot


    @command()
    async def report(self, ctx):
        """Submits a report to the admins"""
        reporter = ctx.message.author

        def check(m):
            if isinstance(m.channel, discord.DMChannel):
                return m.author == reporter

        if not isinstance(ctx.message.channel, discord.DMChannel):
            await ctx.message.delete()
        dm = await ctx.message.author.send(
            "Please select one of the following categories.[CATAGORY 💩 CATAGORY ONE CATAGORY CATAGORY]")
        msg = await self.bot.wait_for('message', timeout=120, check=check)
        dm = await ctx.message.author.send("Good")



def setup(bot):
    bot.add_cog(Reporting(bot))
