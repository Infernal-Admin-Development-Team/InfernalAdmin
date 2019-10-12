"""
This is the main bot file
"""
import json

from discord.ext import commands

from bot_modules.welcome import Welcome
from bot_modules.auto_update import AutoUpdate

class InfernalAdminClient(commands.Bot):
    """
    Main Infernal Admin Class
    This defines the main entry points for messages
    """

    def __init__(self, c_file, *args, **kwargs):
        with open(c_file) as f:
            self.config=json.load(f)
        f.close()

        super(InfernalAdminClient, self).__init__(command_prefix = commands.when_mentioned_or('$'),
                                                  description='InfernalAdmin')





        self.add_cog(AutoUpdate(self))
        self.event(self.on_ready)

        # self.bg_task = self.loop.create_task(self.my_background_task())



    async def on_ready(self):

        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')




    def begin(self):

        self.run(self.config['token'])

