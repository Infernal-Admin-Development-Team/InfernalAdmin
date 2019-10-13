import json
from collections import namedtuple

# Reading the config file and putting it into a global variable
with open("config.json") as f:
    CONFIG=json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
f.close()


# Simple helper that can be called in the various modules
def is_owner(ctx):
    return ctx.message.author.id == int(CONFIG.owner_id)
