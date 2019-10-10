from discord.ext import commands

from InfernalAdmin.bot import InfernalAdminClient

bot = InfernalAdminClient(c_file="infernal_admin_config_prod.json", command_prefix=commands.when_mentioned_or("a!"),
                          description='InfernalAdmin')
