from discord.ext import commands
from pathlib import Path
import os
from github import Github
from subprocess import check_call as run
class BotModule(commands.Cog):
    """Base Bot module"""

    def __init__(self, bot):
        self.bot = bot

