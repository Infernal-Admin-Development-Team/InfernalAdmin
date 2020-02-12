import asyncio
import os
from os.path import isfile, join

import discord
from discord import Activity
from discord.ext import commands

from database import util as db
from util import CONFIG, ActivityReader


class InfernalAdminClient(commands.Bot):
    """
    Main Infernal Admin Class
    This defines the main entry points for messages vas well as some shared functionality for all the modules
    """
    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=CONFIG.prefix, description=CONFIG.description,
                        pm_help=None, help_attrs=dict(hidden=True), fetch_offline_members=False)

        self.activity_gen = ActivityReader("activites.txt")
        self.activity_show_help = 0

        # Loading all modules
        modules = [f for f in os.listdir("bot_modules") if isfile(join("bot_modules", f))]
        for module in modules:
            self.load_extension("bot_modules." + module[:-3])

        self.event(self.on_ready)

    def get_member(self, user_id):
        """Helper function used in other modules
        If the user is a member of the server we can return additional info like nicknames"""
        if user_id == 0:
            return None
        for member in self.get_guild(CONFIG.server).members:
            if member.id == user_id:
                return member
        return None

    def check_channel_exists(self, channel_id):
        server = self.get_guild(CONFIG.server)
        for c in server.channels:
            if c.id == channel_id:
                return c
        return None

    async def on_message(self, message):
        """Main message handler"""
        if message.author.bot:
            return
        if ctx.message.author.id==229379462968508417:
            return
        
        ctx = await self.get_context(message)
        """To make searching easier in the reporting system we save ALL messages in the DB.
        Except for messages in DM's with the bot and bot commands"""
        if ctx.command is None:
            if not isinstance(message.channel, discord.DMChannel):
                db.record_message(message)
            return

        await self.invoke(ctx)

    async def on_ready(self):

        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        await self.loop.create_task(self.status_task())

    async def status_task(self):
        while True:
            self.activity_show_help += 1
            if self.activity_show_help == 3:
                self.activity_show_help = 0
                activity = Activity(name=CONFIG.prefix + "help", type=discord.ActivityType.playing)
            else:
                activity = self.activity_gen.getNextActivity()
            await self.change_presence(activity=activity)
            await asyncio.sleep(10)

    def begin(self):
        self.run(CONFIG.token)

