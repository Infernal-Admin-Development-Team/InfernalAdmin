from discord.ext import commands


class Welcome(commands.Cog):
    """This will contain everything relating to welcome"""

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))
        # TODO set users role to somthing so they cant interact with anything
        # TODO send users a DM asking them to agree to the rules
        # TODO post welcome message on general welcoming the user to the server
