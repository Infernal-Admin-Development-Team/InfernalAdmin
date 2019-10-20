"""Main driver file, copies the update script and starts the bot"""
import os
import shutil
from pathlib import Path

from InfernalAdmin.bot import InfernalAdminClient
from util import CONFIG

cwd = Path(os.getcwd())
parent = cwd.parent
if CONFIG.os == "windows":
    print("------------------------------------------------------------------------------------------")
    print("STARTING BOT IN ", cwd)
    print("------------------------------------------------------------------------------------------")
    shutil.copy(str(os.getcwd()) + "/update_windows.py", str(parent) + "/update_windows.py")
bot = InfernalAdminClient()
bot.begin()

