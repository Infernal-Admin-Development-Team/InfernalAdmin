import json
import logging
import random
from collections import namedtuple

import discord

import database as db

# Reading the config file and putting it into a global variable
with open("config.json") as f:
    CONFIG=json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
f.close()

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename=CONFIG.logfile, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Simple helper that can be called in the various modules
def is_owner(ctx):
    return ctx.message.author.id == int(CONFIG.owner_id)


def can_view_reports(ctx):
    s = db.session()
    can_do = False
    for r in ctx.message.author.roles:
        role = s.query(db.AdminRole).filter(db.AdminRole.role_id == r.id).first()
        if role and role.perms >= 1:
            can_do = True
            break
    s.close()
    return can_do


def can_comment_reports(ctx):
    s = db.session()
    can_do = False
    for r in ctx.message.author.roles:
        role = s.query(db.AdminRole).filter(db.AdminRole.role_id == r.id).first()
        if role and role.perms >= 2:
            can_do = True
            break
    s.close()
    return can_do


def can_resolve_reports(ctx):
    s = db.session()
    can_do = False
    for r in ctx.message.author.roles:
        role = s.query(db.AdminRole).filter(db.AdminRole.role_id == r.id).first()
        if role and role.perms >= 3:
            can_do = True
            break
    s.close()
    return can_do


def is_admin(ctx):
    s = db.session()
    user_is_admin = False
    for r in ctx.message.author.roles:
        report = s.query(db.AdminRole).filter(db.AdminRole.role_id == r.id).first()
        if report:
            user_is_admin = True
            break
    s.close()
    return user_is_admin
def report_type_to_str(type):
    types = ["admin abuse", "dispute between users", "spam", "bot abuse", "harassment", "server issue"]
    return types[type]


def get_link_to_channel(channel_id):
    return "http://discordapp.com/channels/" + str(CONFIG.server) + "/" + str(channel_id)

def report_status_to_str(status):
    types = ["OPEN", "RESOLVED", "REJECTED", "IN PROGRESS"]
    return types[status]

class ActivityReader:
    def __init__(self, filename):
        self.activity_list = []
        with open(filename) as f:
            self.activity_list = f.readlines()
        f.close()

    def getNextActivity(self):

        index = random.randint(0, len(self.activity_list) - 1)
        activity = self.activity_list[index]
        ret_num = int(activity[0])
        ret_str = activity[4:-2]
        type = None

        if ret_num == 0:
            type = discord.ActivityType.playing
        elif ret_num == 1:
            type = discord.ActivityType.watching
        elif ret_num == 2:
            type = discord.ActivityType.listening
        else:
            type = discord.ActivityType.streaming
        return discord.Activity(name=ret_str, type=type)
