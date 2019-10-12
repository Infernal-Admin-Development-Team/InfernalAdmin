#from discord.ext import commands
#from bot_modules.auto_update import AutoUpdate

from InfernalAdmin.bot import InfernalAdminClient


bot = InfernalAdminClient(c_file="infernal_admin_config.json")


bot.begin()

