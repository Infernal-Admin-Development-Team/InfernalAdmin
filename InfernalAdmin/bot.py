"""
This is the main bot file
"""
import json

from discord.ext import commands

from bot_modules.welcome import Welcome


class InfernalAdminClient(commands.Bot):
    """
    Main Infernal Admin Class
    This defines the main entry points for messages
    """

    def __init__(self, c_file, *args, **kwargs):
        super(InfernalAdminClient, self).__init__(*args, **kwargs)

        self.add_cog(Welcome(self))


        with open(c_file) as f:
            self.config=json.load(f)
        f.close()

        self.event(self.on_message)
        self.event(self.on_ready)
        # self.bg_task = self.loop.create_task(self.my_background_task())
        self.run(self.config['token'])

    async def on_ready(self):

        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self,message):
        pass
