"""Main driver file, copies the update script and starts the bot"""
import os
import shutil
from pathlib import Path

from InfernalAdmin.bot import InfernalAdminClient

cwd = Path(os.getcwd())
parent = cwd.parent

print("------------------------------------------------------------------------------------------")
print("STARTING BOT IN ", cwd)
print("------------------------------------------------------------------------------------------")
shutil.copy(str(os.getcwd()) + "/update_windows.py", str(parent) + "/update_windows.py")
shutil.copy(str(os.getcwd()) + "/update_linux.py", str(parent) + "/update_linux.py")
bot = InfernalAdminClient()
bot.begin()

