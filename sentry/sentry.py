# Ivysalt's sentry module. It keeps track of people who join and leave a chat.
# LICENSE: This single module is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# @category   Tools
# @copyright  Copyright (c) 2018 dpc
# @version    1.1
# @author     dpc

import asyncio
import json
import os

from discord.ext import commands
from cogs.utils import checks
from cogs.utils.dataIO import fileIO


joinleave_path = 'data/sentry/joinleave.json'
bans_path = 'data/sentry/bans.json'


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
    folders = ["data/sentry"]
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    default = {}
    if not os.path.isfile(joinleave_path):
        print("Creating joinleave.json")
        fileIO(joinleave_path, "save", default)
    if not os.path.isfile(bans_path):
        print("Creating bans.json")
        fileIO(bans_path, "save", default)


# validating data
check_folders()
check_files()


with open(joinleave_path) as joinleave_file:
    joinleave_data = json.load(joinleave_file)


with open(bans_path) as sentry_file:
    sentry_bans = json.load(sentry_file)


def save(path, data):
    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def full_inspection(self):
    for server in self.bot.servers:
        if (server.id in sentry_bans):
            for member in server.members:
                if (member.id in sentry_bans[server.id]):
                    yield from self.bot.send_message(member, "```geeettttttt dunked on!!!\nif we're really friends, you won't come back.```")
                    yield from (asyncio.sleep(2))
                    yield from self.bot.ban(member, 7)
                    print("Banning user {0}#{2} with ID {3} from {1}...".format(member.name, server.name, member.discriminator, member.id))


def member_inspection(self, member):
    if (member.server.id in sentry_bans):
        if (member.id in sentry_bans[member.server.id]):
            yield from self.bot.send_message(member, "```geeettttttt dunked on!!!\nif we're really friends, you won't come back.```")
            yield from (asyncio.sleep(2))
            yield from self.bot.ban(member, 7)
            print("Banning user {0} from {1}...".format(member.name, member.server.name, member.discriminator, member.id))
        else:
            print("coast is clear 2")
    else:
        print("coast is clear 1")

class Sentry:
    """Adds various sentry commands.\nThis module was written specifically for a few servers."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(ban_members=True)
    @asyncio.coroutine
    def preban(self, ctx, user_id: str):
        """Users added with this command will be banned on sight.\n"""
        """Only admins may use this command."""
        # adding user id to the ban list
        if is_int(user_id):
            if (ctx.message.server.id in sentry_bans):
                if (user_id in sentry_bans[ctx.message.server.id]):
                    yield from self.bot.say("That user is already pre-banned from this server.")
                else:
                    sentry_bans[ctx.message.server.id].append(user_id)
                    save(bans_path, sentry_bans)
                    yield from self.bot.say("User has been pre-banned from this server.")
            else:
                sentry_bans[ctx.message.server.id] = [user_id]
                save(bans_path, sentry_bans)
                yield from self.bot.say("User has been pre-banned from this server.")
        else:
            yield from self.bot.say("Improper command usage.")
        # checking if user's already in the server, and banning them if they are
        for member in ctx.message.server.members:
            member_inspection(self, member)

    @commands.command(pass_context=True, no_pm=True, description=
            "Note: users that have been already banned will not be unbanned.")
    @checks.admin_or_permissions(ban_members=True)
    @asyncio.coroutine
    def unpreban(self, ctx, user_id: str):
        """Users removed with this command will not be banned on sight.\n"""
        """Only admins may use this command."""
        if (ctx.message.server.id in sentry_bans):
            if (user_id in sentry_bans[ctx.message.server.id]):
                sentry_bans[ctx.message.server.id].remove(user_id)
                save(bans_path, sentry_bans)
                yield from self.bot.say("User removed from pre-ban list on this server.")
            else:
                yield from self.bot.say("User is not pre-banned on this server.")
        else:
            yield from self.bot.say("User is not pre-banned on this server.")

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(ban_members=True)
    @asyncio.coroutine
    def setannounce(self, ctx, channel: str = "current"):
        """Sets the bot to announce server's new arrivals in this channel.\n"""
        """Only admins may use this command."""
        # parses the input
        if (len(ctx.message.channel_mentions) == 1):
            channel_id = ctx.message.channel_mentions[0].id
        elif is_int(channel):
            channel_id = channel
        elif channel == "current":
            channel_id = ctx.message.channel
        else:
            yield from self.bot.say("Sorry, I don't know what channel that is.")
            return

        # assigns the announce channel
        if (ctx.message.server.id in joinleave_data):
            joinleave_data[ctx.message.server.id]["announce_channel"] = channel_id
            save(joinleave_path, joinleave_data)
            yield from self.bot.say("Saved announce channel with ID {}.".format(channel_id))
        else:
            joinleave_data[ctx.message.server.id] = {"announce_channel": channel_id, "autoassign_role": ""}
            save(joinleave_path, joinleave_data)
            yield from self.bot.say("Saved announce channel with ID {}.".format(channel_id))

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(ban_members=True)
    @asyncio.coroutine
    def delannounce(self, ctx):
        """Sets the bot to *not* announce new arrivals in this server.\n"""
        """Only admins may use this command."""
        # assigns the announce channel
        if (ctx.message.server.id in joinleave_data):
            joinleave_data[ctx.message.server.id]["announce_channel"] = ""
            yield from self.bot.say("Removed announce channel for this server.")
        else:
            joinleave_data[ctx.message.server.id] = {"announce_channel": "", "autoassign_role": ""}


    @asyncio.coroutine
    def on_member_join(self, member):
        member_inspection(self, member)
        if (member.server.id in joinleave_data):
            yield from self.bot.send_message(member.server.get_channel(joinleave_data[ctx.message.server.id]["announce_channel"]),"{0}#{1}, with user ID {2}, just joined {3}!".format(member.name, member.discriminator, member.id, member.server.name))


    @asyncio.coroutine
    def on_member_leave(self, member):
        member_inspection(self, member)
        if (member.server.id in joinleave_data):
            yield from self.bot.send_message(member.server.get_channel(joinleave_data[ctx.message.server.id]["announce_channel"]),"{0}#{1}, with user ID {2} just left {3}!".format(member.name, member.discriminator, member.id, member.server.name))


    @asyncio.coroutine
    def on_ready(self):
        full_inspection(self)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Sentry(bot))
