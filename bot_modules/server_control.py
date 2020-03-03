from discord.ext.commands import Cog, command, check

from util import *


class ServerControl(Cog):
    """"General propose module for managing roles, spamming, bot permissions.etc"""

    def __init__(self, bot):
        self.bot = bot

    @command()
    @check(is_owner)
    async def setoperator(self, ctx, role_id: int, perms: int):
        """grants permissions to a role to be able to interact with the report system
        USAGE: <ROLE_ID> 0 removes the role from the bot permissions
        USAGE: <ROLE_ID> 1 allows the role to view reports only
        USAGE: <ROLE_ID> 2 allows the role to view and comment on reports
        USAGE: <ROLE_ID> 3 allows the role to view comment, send messages to the reporter and change the status
        """
        s = db.session()
        role = s.query(db.AdminRole).filter(db.AdminRole.role_id == role_id).first()
        if role:
            if perms == 0:
                s.delete(role)
            else:
                role.perms = perms
        else:
            s.add(db.AdminRole(role_id=role_id, perms=perms))
        s.commit()
        s.close()
        await ctx.send("Role set")

    @command()
    @check(is_owner)
    async def getoldusers(self, ctx):
        s = db.session()
        for member in self.bot.get_guild(CONFIG.server).members:

            message = s.query(db.Message).filter(db.Message.author == member.id).first()
            if not message:
                if not member.bot:
                    await ctx.send("No messages from " + member.name)

    @command()
    @check(is_owner)
    async def kickoldusers(self, ctx):
        """As of right now it only gets users who did not post on the server since the bot went online"""
        s = db.session()

        for member in self.bot.get_guild(CONFIG.server).members:

            message = s.query(db.Message).filter(db.Message.author == member.id).first()
            if not message:
                if not member.bot:
                    server = self.bot.get_guild(CONFIG.server)

                    print(server.system_channel)
                    inviteLink = await self.bot.get_guild(CONFIG.server).system_channel.create_invite(xkcd=True,
                                                                                                      max_uses=1)

                    await ctx.send("No messages from " + member.name)
                    await member.send(
                        "You have been kicked from Inferno games because you have not posted anything for a few months")
                    await member.send("If you feel this was a mistake you can rejoin by clicking " + str(inviteLink))
                    await member.kick()
        s.close()

    @command()
    @check(is_owner)
    async def listoperators(self, ctx):
        s = db.session()
        roles = s.query(db.AdminRole)
        for r in roles:
            server_role_list = (await self.bot.fetch_guild(CONFIG.server)).roles
            for rr in server_role_list:
                if rr.id == r.role_id:
                    await ctx.send("Name:" + rr.name + "," + str(r.role_id) + "," + str(r.perms))
                    break
        s.close()
def setup(bot):
    bot.add_cog(ServerControl(bot))

