# Logger based on an old version of Panopticon // https://github.com/ihaveamac/panopticon
# LICENSE: This module is licenced under Apache License 2.0
# @category   Tools
# @copyright  Copyright (c) 2018 dpc
# @version    1.1
# @author     dpc

import asyncio
import base64
from datetime import datetime
from datetime import timezone
import os
import re
import gzip
import signal
import sys
import json
from pathlib import Path

import discord
from discord.enums import ChannelType
from cogs.utils.dataIO import fileIO
from cogs.utils import checks

from discord.ext import commands


def save_logs(filename, data):
    full_path = Path('data/logger/invoked_logs/' + filename)
    if full_path.is_file():
        with open(str(full_path), "rb") as original:
            old_data = original.read()
        with open(str(full_path), "wb") as log_file:
            log_file.write(data.encode("utf8") + old_data)
    else:
        with open(str(full_path), "wb") as log_file:
            log_file.write(data.encode("utf8"))


# Panopticon functions go here

# Translate Red's settings into Panopticon's settings (removed in favour of find/replace outright)
#USE_LOCALTIME = settings.use_localtime
#LOG_DIR = settings.log_dir
#MAX_MESSAGES = settings.max_messages


# This sanitizes an input string to remove characters that aren't valid
#   in filenames. There are a lot of other bad filenames that can appear,
#   but given the predictable nature of our input in this application,
#   they aren't handled here.
def clean_filename(string):
    return re.sub(r'[/\\:*?"<>|\x00-\x1f]', '', string)


# This builds the relative file path & filename to log to,
#   based on the channel type of the message.
# It is affixed to the log directory set in config.py
def make_filename(self, message):
    if message.edited_timestamp:
        time = message.edited_timestamp
    else:
        time = message.timestamp
    timestamp = time.strftime('%F')
    if message.channel.type == ChannelType.text:
        return "{0}/{2}-{1}/#{4}-{3}/{5}.log".format(
            self.settings["log_dir"],
            clean_filename(message.server.name),
            message.server.id,
            clean_filename(message.channel.name),
            message.channel.id,
            timestamp
        )
    elif message.channel.type == ChannelType.private:
        return "{0}/DM/{2}-{1}/{3}.log".format(
            self.settings["log_dir"],
            clean_filename(message.channel.user.name),
            message.channel.user.id,
            timestamp
        )
    elif message.channel.type == ChannelType.group:
        return "{0}/GROUP/{2}-{1}/{3}.log".format(
            self.settings["log_dir"],
            clean_filename(message.channel.name),
            message.channel.id,
            timestamp
        )


# Uses a Message object to build a very pretty string.
# Format:
#   (messageid) [21:30:00] <user#0000> hello world
# Message ID will be base64-encoded since it becomes shorter that way.
# If the message was edited, prefix messageid with E:
#   and use the edited timestamp and not the original.
def make_message(self, message):
    # Wrap the message ID in brackets, and prefix E: if the message was edited.
    # Also, base64-encode the message ID, because it's shorter.
    #   This uses less space on disk, and is easier to read in console.
    message_id = '[E:' if message.edited_timestamp else '['
    message_id += "{}]".format(base64.b64encode(
        int(message.id).to_bytes(8, byteorder='little')
    ).decode('utf-8'))

    # Get the datetime from the message
    # If necessary, tell the naive datetime object it's in UTC
    #   and convert to localtime
    if message.edited_timestamp:
        time = message.edited_timestamp
    else:
        time = message.timestamp
    if self.settings["use_localtime"]:
        time = time.replace(tzinfo=timezone.utc).astimezone(tz=None)

    # Convert the datetime to a string in [21:30:00] format
    timestamp = time.strftime('[%H:%M:%S]')

    # Get the author's name, in distinct form, and wrap it
    # in IRC-style brackets
    author = "<{}#{}>".format(
        message.author.name,
        message.author.discriminator
    )

    # Get the message content. Use `.clean_content` to
    #   substitute mentions for a nicer format
    content = message.clean_content.replace('\n', '\n(newline) ')

    # If the message has attachments, grab their URLs
    # attachments = '\n(attach) '.join(
    #     [attachment['url'] for attachment in message.attachments]
    # )
    attachments = ''
    if message.attachments:
        for attach in message.attachments:
            attachments += '\n(attach) {0[url]}'.format(attach)

    # Use all of this to return as one string
    return("{} {} {} {} {}".format(
        message_id,
        timestamp,
        author,
        content,
        attachments
    ))


# Append to file, creating path if necessary
def write(filename, string):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a', encoding='utf8') as file:
        file.write(string + "\n") 
        #print(string, file=file)

# Panopticon functions end here


class Logger:
    """Logs messages neatly into a folder.\n"""
    """Based on https://github.com/ihaveamac/panopticon"""

    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/logger/settings.json", 'load')

    def save_settings(self):
        fileIO('data/logger/settings.json', 'save', self.settings)


    @commands.command(pass_context=True, aliases=["loglastdisk"], hidden=True)
    @checks.admin_or_permissions(ban_members=True)
    async def log_last_disk(self, ctx, messages: int = 100):
        """Logs previous messages in a channel.\nDefaults to 100 messages, limit is 1000."""
        if messages < 1:
            await self.bot.say("Nice try :P")
            return
        elif messages > 1000:
            await self.bot.say("Yeah, I don't think so.")

        await self.bot.say("Starting logging...")

        if (str(ctx.message.channel.type) == "private"):
            filename = 'DM-({6})-{0:04d}{1:02d}{2:02d}-{3:02d}-{4:02d}-{5:02d}.log'.format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, ",".join(ctx.message.channel.recipients))
            intro = "Log started by {6} on {0:04d}/{1:02d}/{2:02d} at {3:02d}:{4:02d}:{5:02d} with recipient {7}.\nUser ID: {8}\nChannel ID: {9}\nChannel type: {10}\n".format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, ctx.message.author.name, ", ".join(ctx.message.channel.recipients), ctx.message.author.id, ctx.message.channel.id, ctx.message.channel.type)
        elif (str(ctx.message.channel.type) == "group"):
            filename = 'Group-{6}-({7})-{0:04d}{1:02d}{2:02d}-{3:02d}-{4:02d}-{5:02d}.log'.format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, ctx.message.channel.name, ",".join(ctx.message.channel.recipients))
            intro = "Log started by {6} on {0:04d}/{1:02d}/{2:02d} at {3:02d}:{4:02d}:{5:02d} in channel {7} with recipients {8}.\nUser ID: {9}\nChannel ID: {10}\nChannel type: {11}\n".format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, ctx.message.author.name, ctx.message.channel.name, ", ".join(ctx.message.channel.recipients), ctx.message.author.id, ctx.message.channel.id, ctx.message.channel.type)
        else:
            filename = 'Server-{6}-{7}-{0:04d}{1:02d}{2:02d}-{3:02d}-{4:02d}-{5:02d}.log'.format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, ctx.message.server.name, ctx.message.channel.name)
            intro = "Log started by {6} on {0:04d}/{1:02d}/{2:02d} at {3:02d}:{4:02d}:{5:02d} in channel {7} on server {8}.\nUser ID: {9}\nChannel ID: {10}\nServer ID: {11}\nChannel type: {12}\n".format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, str(ctx.message.author), str(ctx.message.channel), str(ctx.message.server), ctx.message.author.id, ctx.message.channel.id, ctx.message.server.id, ctx.message.channel.type)

        async for message in self.bot.logs_from(ctx.message.channel, messages):
            save_logs(filename, make_message(self, message) + "\n")
            #save_logs(filename, "[{0:04d}/{1:02d}/{2:02d}-{3:02d}:{4:02d}:{5:02d}] <{6}> {7}\n".format(message.timestamp.year, message.timestamp.month, message.timestamp.day, message.timestamp.hour, message.timestamp.minute, message.timestamp.second, message.author.name.encode('ascii', 'backslashreplace').decode('ascii'), message.content.encode('ascii', 'backslashreplace').decode('ascii')))

        save_logs(filename, intro)

        with open("data/logger/invoked_logs/"+filename,"rb") as f_in, gzip.open("data/logger/invoked_logs/"+filename+'.gz', 'wb') as f_out:
            f_out.writelines(f_in)

        with open("data/logger/invoked_logs/"+filename+".gz","rb") as f_out:
            await self.bot.send_file(ctx.message.channel, f_out, content="Log successfuly written.")


    @commands.command(pass_context=True, aliases=["loglastmem","loglast","log_last"])
    @checks.admin_or_permissions(ban_members=True)
    async def log_last_mem(self, ctx, messages: int = 100):
        """Logs previous messages in a channel.\nDefaults to 100 messages but has no limit (theoretically)."""
        if messages < 1:
            await self.bot.say("Nice try :P")
            return

        await self.bot.say("Starting logging...")

        if (str(ctx.message.channel.type) == "private"):
            filename = 'DM-({6})-{0:04d}{1:02d}{2:02d}-{3:02d}-{4:02d}-{5:02d}.log'.format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, ",".join(ctx.message.channel.recipients))
            intro = "Log started by {6} on {0:04d}/{1:02d}/{2:02d} at {3:02d}:{4:02d}:{5:02d} with recipient {7}.\nUser ID: {8}\nChannel ID: {9}\nChannel type: {10}\n".format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, ctx.message.author.name, ", ".join(ctx.message.channel.recipients), ctx.message.author.id, ctx.message.channel.id, ctx.message.channel.type)
        elif (str(ctx.message.channel.type) == "group"):
            filename = 'Group-{6}-({7})-{0:04d}{1:02d}{2:02d}-{3:02d}-{4:02d}-{5:02d}.log'.format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, ctx.message.channel.name, ",".join(ctx.message.channel.recipients))
            intro = "Log started by {6} on {0:04d}/{1:02d}/{2:02d} at {3:02d}:{4:02d}:{5:02d} in channel {7} with recipients {8}.\nUser ID: {9}\nChannel ID: {10}\nChannel type: {11}\n".format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, ctx.message.author.name, ctx.message.channel.name, ", ".join(ctx.message.channel.recipients), ctx.message.author.id, ctx.message.channel.id, ctx.message.channel.type)
        else:
            filename = 'Server-{6}-{7}-{0:04d}{1:02d}{2:02d}-{3:02d}-{4:02d}-{5:02d}.log'.format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, ctx.message.server.name, ctx.message.channel.name)
            intro = "Log started by {6} on {0:04d}/{1:02d}/{2:02d} at {3:02d}:{4:02d}:{5:02d} in channel {7} on server {8}.\nUser ID: {9}\nChannel ID: {10}\nServer ID: {11}\nChannel type: {12}\n".format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, str(ctx.message.author), str(ctx.message.channel), str(ctx.message.server), ctx.message.author.id, ctx.message.channel.id, ctx.message.server.id, ctx.message.channel.type)

        log_content = ""
        async for message in self.bot.logs_from(ctx.message.channel, messages):
            log_content = make_message(self, message) + "\n" + log_content

        save_logs(filename, intro)

        with open("data/logger/invoked_logs/"+filename,"rb") as f_in, gzip.open("data/logger/invoked_logs/"+filename+'.gz', 'wb') as f_out:
            f_out.writelines(f_in)

        with open("data/logger/invoked_logs/"+filename+".gz","rb") as f_out:
            await self.bot.send_file(ctx.message.channel, f_out, content="Log successfuly written.")


    @asyncio.coroutine
    def on_message(self, message):
        filename = make_filename(self, message)
        string = make_message(self, message)
        write(filename, string)

    # Note from discord.py documentation:
    #   If the message is not found in the Client.messages cache, then these
    #   events will not be called. This happens if the message is too old
    #   or the client is participating in high traffic servers.
    # Through testing, messages from before the current client session also do
    #   not fire the event.
    @asyncio.coroutine
    def on_message_edit(self, _, message):
        filename = make_filename(self, message)
        string = make_message(self, message)
        write(filename, string)


    #Gonna add this later
    # @asyncio.coroutine
    # def on_reaction_add(self, _, message):
    #     filename = make_filename(self, message)
    #     string = make_message(self, message)
    #     write(filename, string)


def check_folders():
    folders = ["data/logger", "data/logger/logs", "data/logger/invoked_logs"]
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    default = {"use_localtime": False, "log_dir": "data/logger/logs"}
    settings_path = "data/logger/settings.json"

    if not os.path.isfile(settings_path):
        print("Creating default logger settings.json...")
        fileIO(settings_path, "save", default)
    else:  # consistency check
        current = fileIO(settings_path, "load")
        if current.keys() != default.keys():
            for key in default.keys():
                if key not in current.keys():
                    current[key] = default[key]
                    print(
                        "Adding " + str(key) + " field to logger settings.json")
            fileIO(settings_path, "save", current)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Logger(bot))
