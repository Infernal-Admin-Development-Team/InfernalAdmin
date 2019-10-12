"""
This is the main bot file
"""
from discord.ext import commands

from util import CONFIG

modules = {
    'auto_update',
    'welcome',
    "reporting"
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

