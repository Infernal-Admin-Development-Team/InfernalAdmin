from discord import Client, Game, Message
import json


class InfernalAdminClient(Client):
    """
    Main Infernal Admin Class
    This defines the main entry points for messages
    """
    def __init__(self, loop, c_file):
        super(InfernalAdminClient, self).__init__()


        with open(c_file) as f:
            self.config=json.load(f)
        f.close()

        self.event(self.on_message)
        self.event(self.on_ready)
        self.loop = loop

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self,message):
        pass
