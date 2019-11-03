import json
import random
from collections import namedtuple

# Reading the config file and putting it into a global variable
with open("config.json") as f:
    CONFIG=json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
f.close()


# Simple helper that can be called in the various modules
def is_owner(ctx):
    return ctx.message.author.id == int(CONFIG.owner_id)


class ActivityReader:
    def __init__(self, filename):
        self.activity_list = []
        with open(filename) as f:
            self.activity_list = f.readlines()
        f.close()

    def getNextActivity(self):
        index = random.randint(0, len(self.activity_list))
        activity = self.activity_list[index]
        ret_num = int(activity[0])
        ret_str = activity[4:-2]
        return ret_num, ret_str
