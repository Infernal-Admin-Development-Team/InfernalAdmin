"""
This is the main bot file
"""
import json
from collections import namedtuple
from discord.ext import commands
from util import CONFIG
from bot_modules.welcome import Welcome
from bot_modules.auto_update import AutoUpdate
modules = {
    'auto_update',
    'welcome'
}

class InfernalAdminClient(commands.Bot):
    """
    Main Infernal Admin Class
    This defines the main entry points for messages
    """

    def __init__(self, c_file, *args, **kwargs):
        super().__init__(command_prefix=CONFIG.prefix, description=CONFIG.description,
                        pm_help=None, help_attrs=dict(hidden=True), fetch_offline_members=False)



        self.event(self.on_ready)

        # self.bg_task = self.loop.create_task(self.my_background_task())

        for module in modules:
            self.load_extension("bot_modules."+module)

    async def on_ready(self):

        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')




    def begin(self):

        self.run(CONFIG.token)

