"""
This is the main bot file
"""
import asyncio
import os
from os.path import isfile, join

import discord
from discord import Activity, Game
from discord.ext import commands

from database import util as db
from util import CONFIG


class InfernalAdminClient(commands.Bot):
    """
    Main Infernal Admin Class
    This defines the main entry points for messages
    """

    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=CONFIG.prefix, description=CONFIG.description,
                        pm_help=None, help_attrs=dict(hidden=True), fetch_offline_members=False)

        """
        TODO replace the below with a call to 
        self.activitys=ActivityReader("someFile.txt")
        """
        self.activities = [Activity(name="with fire", type=discord.ActivityType.playing),
                           Activity(name="Pompanomike closely", type=discord.ActivityType.watching),
                           Activity(name="$help", type=discord.ActivityType.playing),
                           Activity(name="mispaling to motivate mike to join the project.",
                                    type=discord.ActivityType.playing),
                           Activity(name="CHRIS NOISES", type=discord.ActivityType.listening)]

        self.event(self.on_ready)
        modules = [f for f in os.listdir("bot_modules") if isfile(join("bot_modules", f))]

        # self.bg_task = self.loop.create_task(self.my_background_task())
        print(modules)
        for module in modules:
            print(module[:-3])
            self.load_extension("bot_modules." + module[:-3])

    async def process_commands(self, message):
        ctx = await self.get_context(message)

        if ctx.command is None:
            if not isinstance(message.channel, discord.DMChannel):
                db.record_message(message)
            return

        await self.invoke(ctx)

    async def on_message(self, m):
        if m.author.bot:
            return

        """
        To make searching easier in the reporting system we save ALL messages in the DB.
        Unless they are tied to a report the messages are removed if they are older then 48 hours
        """

        await self.process_commands(m)

    async def on_ready(self):

        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        await self.change_presence(activity=Game(name="aaa"))
        await self.loop.create_task(self.status_task())
        # await self.loop.create_task(self.launcher_watchdog())

    # async def launcher_watchdog(self):

    async def status_task(self):
        while True:
            # TODO use self.activityReader.getNextActivity() in here
            for activity in self.activities:
                await self.change_presence(activity=activity)
                await asyncio.sleep(10)

    def begin(self):

        self.run(CONFIG.token)

