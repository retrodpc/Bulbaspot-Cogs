import asyncio
import json
import os
from random import randint

from discord.ext import commands
from .utils import checks
from cogs.utils.dataIO import fileIO


# Checks from Bulbaspot
def kirby25_check(self, message):
    if ((message.channel.id in self.settings["kirby25"]) or
        (message.channel.name in self.settings["kirby25"]) or
        message.channel.is_private):
        return True
    else:
        return False


def not_kirby25_check(self, message):
    if ((message.channel.id in self.settings["kirby25"]) or
        (message.channel.name in self.settings["kirby25"])):
        return False
    else:
        return True


def is_int(s):
    try:
        int(s)
        if float(s) % 1 == 0:
            return True
        else:
            return False
    except ValueError:
        return False


def check_folders():
    folders = ["data/needle"]
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    default = {"kirby25": ['254775363840770049']}
    settings_path = "data/needle/settings.json"

    if not os.path.isfile(settings_path):
        print("Creating default Needle settings.json...")
        fileIO(settings_path, "save", default)
    else:  # consistency check
        current = fileIO(settings_path, "load")
        if current.keys() != default.keys():
            for key in default.keys():
                if key not in current.keys():
                    current[key] = default[key]
                    print(
                        "Adding " + str(key) + " field to Needle settings.json")
            fileIO(settings_path, "save", current)


check_folders()
check_files()


with open('data/needle/settings.json') as needle_file:
    needle_bans = json.load(needle_file)


def save(data):
    with open('data/needle/settings.json', "w") as needle_file:
        json.dump(data, needle_file, indent=4)


class Needle:
    """Adds various needle commands.\nThis module was written specifically for a server."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/needle/settings.json", 'load')

    def save_settings(self):
        fileIO('data/needle/settings.json', 'save', self.settings)


    @asyncio.coroutine
    def on_message(self, message):
        if ((kirby25_check(self, message)) and (message.author != self.bot.user)):
            word_list = message.content.lower().split()
            if ("y'all" in word_list) or ("yall" in word_list):
                yield from self.bot.send_message(message.channel, '*you all')
            elif ((message.content.lower().startswith('ok') != True) and
                    ((message.author.id == "220438641439277056")  or (randint(1,25) == 13)) and
                    ((len(word_list) == 1) or (randint(1,25) == 13))):
                yield from self.bot.send_message(message.channel, 'hi liam')


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Needle(bot))
