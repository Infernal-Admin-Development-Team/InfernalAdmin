"""Main driver file, copies the update script and starts the bot"""
import logging
import os
import shutil
from pathlib import Path

from InfernalAdmin.bot import InfernalAdminClient
from util import CONFIG
print("hi")
log = logging.getLogger(__name__)
cwd = Path(os.getcwd())
parent = cwd.parent
if CONFIG.os == "windows":
    shutil.copy(str(os.getcwd()) + "/update_windows.py", str(parent) + "/update_windows.py")

bot = InfernalAdminClient()
bot.begin()
