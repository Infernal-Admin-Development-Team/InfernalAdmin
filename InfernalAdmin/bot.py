"""
This is the main bot file
"""
import asyncio
import os
from os.path import isfile, join

import discord
from discord import Activity, Game
from discord.ext import commands

from util import CONFIG


class InfernalAdminClient(commands.Bot):
    """
    Main Infernal Admin Class
    This defines the main entry points for messages
    """

    def __init__(self, *args, **kwargs):
        super().__init__(command_prefix=CONFIG.prefix, description=CONFIG.description,
                        pm_help=None, help_attrs=dict(hidden=True), fetch_offline_members=False)

        self.activities = [Activity(name="with fire", type=discord.ActivityType.playing),
                           Activity(name="Pompanomike closely", type=discord.ActivityType.watching),
                           Activity(name="CHRIS NOISES", type=discord.ActivityType.listening)]
        self.event(self.on_ready)
        modules = [f for f in os.listdir("bot_modules") if isfile(join("bot_modules", f))]

        # self.bg_task = self.loop.create_task(self.my_background_task())
        print(modules)
        for module in modules:
            print(module[:-3])
            self.load_extension("bot_modules." + module[:-3])



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
            for activity in self.activities:
                await self.change_presence(activity=activity)
                await asyncio.sleep(10)




    def begin(self):

        self.run(CONFIG.token)

