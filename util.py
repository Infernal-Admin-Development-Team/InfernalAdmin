import json
from collections import namedtuple
with open("infernal_admin_config.json") as f:
    CONFIG=json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
f.close()

def is_owner(ctx):
    print(ctx.message.author.id)
    return ctx.message.author.id == int(CONFIG.owner_id)
    #return True