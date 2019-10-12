#from discord.ext import commands
#from bot_modules.auto_update import AutoUpdate

import os
import shutil
from pathlib import Path

from InfernalAdmin.bot import InfernalAdminClient

cwd = Path(os.getcwd())
parent = cwd.parent

shutil.copy(os.path.join(os.getcwd() + "update_windows.py"), os.path.join(parent, "update_windows.py"))
bot = InfernalAdminClient()


bot.begin()

