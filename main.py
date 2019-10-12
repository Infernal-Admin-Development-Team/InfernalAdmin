#from discord.ext import commands
#from bot_modules.auto_update import AutoUpdate

import os
import shutil
from pathlib import Path

from InfernalAdmin.bot import InfernalAdminClient

cwd = Path(os.getcwd())
parent = cwd.parent

shutil.copy(str(os.getcwd()) + "\\update_windows.py", str(parent) + "\\update_windows.py")
bot = InfernalAdminClient()


bot.begin()

