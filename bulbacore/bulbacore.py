# Adds core commands formerly from Bulbaspot. This adds mostly expression and shiptoast commands.
# LICENSE: This module is licenced under Apache License 2.0
# @category   Tools
# @copyright  Copyright (c) 2018 dpc
# @version    1.1
# @author     dpc

import asyncio
from base64 import standard_b64decode, standard_b64encode
import json
from math import floor
import os
from pathlib import Path
import random
from random import randint
from string import ascii_letters, digits

from discord.ext import commands

from cogs.utils import checks
from cogs.utils.dataIO import fileIO


# Import the copypasta data
with open('data/bulbacore/copypasta.json') as copypasta_file:    
    copypastas = json.load(copypasta_file)


# Checks from Bulbaspot
def shiptoast_check(self, message):
    if (message.channel.id in self.settings["shiptoast"]) or (message.channel.name in self.settings["shiptoast"]) or message.channel.is_private:
        return True
    else:
        return False


def not_shiptoast_check(self, message):
    if (message.channel.id in self.settings["shiptoast"]) or (message.channel.name in self.settings["shiptoast"]):
        return False
    else:
        return True


def name_sanitize(name):
    return "".join([ch for ch in name if ch in (ascii_letters + digits + "-_")])


def is_int(s):
    try:
        int(s)
        if float(s) % 1 == 0:
            return True
        else:
            return False
    except ValueError:
        return False


def zalgo_gen(text):
    text = str(text)
    if len(text) <= 666:
        chara = ['\u030D', '\u030E', '\u0304', '\u0305', '\u033F',
                 '\u0311', '\u0306', '\u0310', '\u0352', '\u0357',
                 '\u0351', '\u0307', '\u0308', '\u030A', '\u0342',
                 '\u0343', '\u0344', '\u034A', '\u034B', '\u034C',
                 '\u0303', '\u0302', '\u030C', '\u0350', '\u0300',
                 '\u0301', '\u030B', '\u030F', '\u0312', '\u0313',
                 '\u0314', '\u033D', '\u0309', '\u0363', '\u0364',
                 '\u0365', '\u0366', '\u0367', '\u0368', '\u0369',
                 '\u036A', '\u036B', '\u036C', '\u036D', '\u036E',
                 '\u036F', '\u033E', '\u035B', '\u0346', '\u031A',
                 '\u0315', '\u031B', '\u0340', '\u0341', '\u0358',
                 '\u0321', '\u0322', '\u0327', '\u0328', '\u0334',
                 '\u0335', '\u0336', '\u034F', '\u035C', '\u035D',
                 '\u035E', '\u035F', '\u0360', '\u0362', '\u0338',
                 '\u0337', '\u0361', '\u0489',
                 '\u0316', '\u0317', '\u0318', '\u0319', '\u031C',
                 '\u031D', '\u031E', '\u031F', '\u0320', '\u0324',
                 '\u0325', '\u0326', '\u0329', '\u032A', '\u032B',
                 '\u032C', '\u032D', '\u032E', '\u032F', '\u0330',
                 '\u0331', '\u0332', '\u0333', '\u0339', '\u033A',
                 '\u033B', '\u033C', '\u0345', '\u0347', '\u0348',
                 '\u0349', '\u034D', '\u034E', '\u0353', '\u0354',
                 '\u0355', '\u0356', '\u0359', '\u035A', '\u0323']
        character_set = []
        final_output = ""
        top_kek = floor(2000 / float(len(text)))
        if top_kek > 25:
            top_kek = 25
        for i in range(len(text)):
            character_set.append(text[i])
            for _ in range(top_kek-1):
                character_set[i] = character_set[i] + chara[randint(0,len(chara)-1)]
            final_output = final_output + character_set[i]
        return final_output
    else:
        return "Sorry but my spoops won't fit in here. \U0001F47B"


# Generates a text penis at a given length
def this_gen(length):
    if (is_int(length) is False):
        return "8================D"
    else:
        length = int(length)
        if (length <= 1998 and length >= 0):
            this_thing = "8"
            for _ in range(length):
                this_thing = this_thing + "="
            this_thing = this_thing + "D"
            return this_thing
        elif (length >= -1998 and length < 0):
            new_length = -length
            this_thing = "D"
            for _ in range(new_length):
                this_thing = this_thing + "="
            this_thing = this_thing + "8"
            return this_thing
        else:
            return "Sorry bud, but my dick won't fit in here. **_: )_**"


# Generates a wow at a given length
def wow_gen(length):
    if (is_int(length) is False):
        return "***__~~woooooooooooooooooooooooooooooow~~__***"
    else:
        length = int(length)
        if (length <= 1984 and length >= 0):
            wow_thing = "***__~~w"
            for _ in range(length):
                wow_thing = wow_thing + "o"
            wow_thing += "w~~__***"
            return wow_thing
        elif (length >= -1984 and length < 0):
            new_length = -length
            wow_thing = "***__~~ʍ"
            for _ in range(new_length):
                wow_thing = wow_thing + "o"
            wow_thing += wow_thing + "ʍ~~__***"
            return wow_thing
        else:
            return "Sorry bud, but your wow is too much for me to handle.\n" \
            "Here's a doge for now: https://upload.wikimedia.org/wikipedia/en/5/5f/Original_Doge_meme.jpg **_: (_**"


# Metal commands will generate a "metal" song represented in text.
def metal():
    primary_metal_chara = "0123456789ABDEGHIJLMNÑOPQRSTVWXYZabcdefghijklmnñpqrstvwxzFUCKyou"
    secondary_metal_chara = "!\"#$%&/()=|"
    primary_solo_frisk = "!#$%&/()=?[]{}:¨|;+¿¡@^\"-.,'°0123457869"
    secondary_solo_frisk = "ABCDEGHIJKNÑQRSVWXYZTOMFULP"
    metal_length = randint(180, 200)
    solo_length = randint(250, 300)
    metal_crusher = ""
    han_solo = ""
    for _ in range(metal_length):
        if randint(0, 9) < 9:
            metal_crusher = metal_crusher + primary_metal_chara[randint(0, len(primary_metal_chara)-1)]
        else:
            metal_crusher = metal_crusher + secondary_metal_chara[randint(0, len(secondary_metal_chara)-1)]
    for _ in range(solo_length):
        if randint(0, 19) < 19:
            han_solo = han_solo + primary_solo_frisk[randint(0, len(primary_solo_frisk)-1)]
        else:
            han_solo = han_solo + secondary_solo_frisk[randint(0, len(secondary_solo_frisk)-1)]
    metal = "**METAL!**\n\n" + metal_crusher + "\n\n***AND NOW THE SOLO!!!***\n\n**___~~" + han_solo + "~~___**"
    return metal

def metal_crazy_a():
    primary_metal_chara = "0123456789ABDEGHIJLMNÑOPQRSTVWXYZabcdefghijklmnñpqrstvwxzFUCKyou        "
    secondary_metal_chara = "        !\"#$%&/()=|"
    metal_length = randint(250, 300)
    metal_crusher = ""
    for _ in range(metal_length):
        if randint(0, 9) < 9:
            metal_crusher = metal_crusher + primary_metal_chara[randint(0, len(primary_metal_chara)-1)]
        else:
            metal_crusher = metal_crusher + secondary_metal_chara[randint(0, len(secondary_metal_chara)-1)]
    return metal_crusher

def metal_crazy_b():
    primary_solo_frisk = "        !#$%&/()=?[]{}:¨|;+¿¡@^\"-.,'°0123457869"
    secondary_solo_frisk = "        ABCDEGHIJKNÑQRSVWXYZTOMFULP"
    solo_length = randint(400, 500)
    han_solo = ""
    for _ in range(solo_length):
        if randint(0, 19) < 19:
            han_solo = han_solo + primary_solo_frisk[randint(0, len(primary_solo_frisk)-1)]
        else:
            han_solo = han_solo + secondary_solo_frisk[randint(0, len(secondary_solo_frisk)-1)]
    return han_solo

def fucc():
    primary_metal_chara =  ["\ud83d\ude00", "\ud83d\ude03", "\ud83d\ude04",
                            "\ud83d\ude01", "\ud83d\ude06", "\ud83d\ude05",
                            "\ud83d\ude02", "\ud83e\udd23", "\u263a",
                            "\ud83d\ude0a", "\ud83d\ude07", "\ud83d\ude42",
                            "\ud83d\ude43", "\ud83d\ude09", "\ud83d\ude0c",
                            "\ud83d\ude0d", "\ud83d\ude18", "\ud83d\ude17",
                            "\ud83d\ude19", "\ud83d\ude1a", "\ud83d\ude0b",
                            "\ud83d\ude1c", "\ud83d\ude1d", "\ud83d\ude1b",
                            "\ud83e\udd11", "\ud83e\udd17", "\ud83e\udd13",
                            "\ud83d\ude0e", "\ud83e\udd21", "\ud83e\udd20",
                            "\ud83d\ude0f", "\ud83d\ude12", "\ud83d\ude1e",
                            "\ud83d\ude14", "\ud83d\ude1f", "\ud83d\ude15",
                            "\ud83d\ude41", "\u2639", "\ud83d\ude23",
                            "\ud83d\ude16", "\ud83d\ude2b", "\ud83d\ude29",
                            "\ud83d\ude24", "\ud83d\ude20", "\ud83d\ude21",
                            "\ud83d\ude36", "\ud83d\ude10", "\ud83d\ude11",
                            "\ud83d\ude2f", "\ud83d\ude26", "\ud83d\ude27",
                            "\ud83d\ude2e", "\ud83d\ude32", "\ud83d\ude35",
                            "\ud83d\ude33", "\ud83d\ude31", "\ud83d\ude30",
                            "\ud83d\ude28", "\ud83d\ude22", "\ud83d\ude25",
                            "\ud83e\udd24", "\ud83d\ude2d", "\ud83d\ude13",
                            "\ud83d\ude2a", "\ud83d\ude34", "\ud83d\ude44",
                            "\ud83e\udd14", "\ud83e\udd25", "\ud83d\ude2c",
                            "\ud83e\udd10", "\ud83e\udd22", "\ud83e\udd27",
                            "\ud83d\ude37", "\ud83e\udd12", "\ud83e\udd15",
                            "\ud83d\ude08", "\ud83d\udc7f", "\ud83d\udc7f",
                            "\ud83d\udc79", "\ud83d\udc7a", "\ud83d\udc7a",
                            "\ud83d\udca9", "\ud83d\udc7b", "\ud83d\udc80",
                            "\u2620", "\ud83d\udc7d", "\ud83d\udc7e",
                            "\ud83e\udd16", "\ud83c\udf83"]
    secondary_metal_chara = ["\ud83d\udc36", "\ud83d\udc31", "\ud83d\udc2d",
                             "\ud83d\udc39", "\ud83d\udc30", "\ud83e\udd8a",
                             "\ud83d\udc3b", "\ud83d\udc3c", "\ud83d\udc28",
                             "\ud83d\udc2f", "\ud83e\udd81", "\ud83d\udc2e",
                             "\ud83d\udc37", "\ud83d\udc3d", "\ud83d\udc38",
                             "\ud83d\udc35", "\ud83d\ude48", "\ud83d\ude49",
                             "\ud83d\ude4a", "\ud83d\udc12", "\ud83d\udc27",
                             "\ud83d\udc14", "\ud83d\udc26", "\ud83d\udc24",
                             "\ud83d\udc23", "\ud83d\udc25", "\ud83e\udd86",
                             "\ud83e\udd85", "\ud83e\udd89", "\ud83e\udd87",
                             "\ud83d\udc3a", "\ud83d\udc17", "\ud83d\udc34",
                             "\ud83e\udd84", "\ud83c\udf4f", "\ud83c\udf4e",
                             "\ud83c\udf50", "\ud83c\udf4a", "\ud83c\udf4b",
                             "\ud83c\udf4c", "\ud83c\udf49", "\ud83c\udf47",
                             "\ud83c\udf53", "\ud83c\udf48", "\ud83c\udf3d",
                             "\ud83e\udd55", "\ud83c\udf46", "\ud83e\udd52",
                             "\ud83c\udf45", "\ud83e\udd51", "\ud83e\udd5d",
                             "\ud83c\udf4d", "\ud83c\udf51", "\ud83c\udf52",
                             "\ud83c\udf36", "\ud83e\udd54", "\ud83c\udf60",
                             "\ud83c\udf30", "\ud83e\udd5c", "\ud83c\udf6f",
                             "\ud83e\udd50", "\ud83c\udf5e", "\ud83e\udd56",
                             "\ud83e\uddc0", "\ud83c\udf54", "\ud83c\udf2d",
                             "\ud83c\udf55", "\ud83c\udf56", "\ud83c\udf64",
                             "\ud83e\udd5e", "\ud83e\udd53", "\ud83c\udf73",
                             "\ud83e\udd5a", "\ud83c\udf66", "\ud83c\udf70",
                             "\ud83c\udf82", "\ud83c\udf6e", "\ud83c\udf6d",
                             "\ud83c\udf6c", "\ud83c\udf6b", "\ud83c\udf7f",
                             "\ud83c\udf69", "\ud83c\udf6a"]
    metal_length = randint(100, 150)
    metal_crusher = "FUCK ON ME!!!!!!!!!!!!!!!!!!!!! "
    for _ in range(metal_length):
        if randint(0, 10) < 6:
            metal_crusher = metal_crusher + primary_metal_chara[randint(0, len(primary_metal_chara)-1)]
        else:
            metal_crusher = metal_crusher + secondary_metal_chara[randint(0, len(secondary_metal_chara)-1)]
    return metal_crusher


class Bulbacore:
    """Ivysalt's misc. commands ported over from the old Bulbaspot. Please don't abuse."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/bulbacore/settings.json", 'load')

    def save_settings(self):
        fileIO('data/bulbacore/settings.json', 'save', self.settings)

    @commands.command(pass_context=True)
    @asyncio.coroutine
    def zalgo(self, ctx, *, message):
        """spoopy\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(zalgo_gen(message))

    @commands.group(pass_context=True)
    @asyncio.coroutine
    def bulba(self, ctx):
        """Bulba's quote generator\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            if ctx.invoked_subcommand is None:
                yield from self.bot.say(random.choice(copypastas["bulbaquotes"]))
    
    @bulba.command(pass_context=True)
    @asyncio.coroutine
    def list(self, ctx):
        """Bulba's quote list\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say('http://pastebin.com/dvH26JwB')

    @commands.command(pass_context=True, hidden=True, 
            description="wait how the fuck did you find this lmao", aliases=["bulbatts"])
    @asyncio.coroutine
    def bulba_tts(self, ctx):
        """Bulba's quote generator read aloud :P\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(random.choice(copypastas["bulbaquotes"]), tts=True)

    @commands.command(pass_context=True)
    @asyncio.coroutine
    def cheng(self, ctx):
        """Cheng generator\nThis command doesn't work in all channels."""
        cheng = (random.choice(copypastas["cheng_intro"])
                + random.choice(copypastas["cheng_middle"])
                + random.choice(copypastas["cheng_end"]))
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(cheng)

    @commands.command(pass_context=True,hidden=True,description="wait how the fuck did you find this lmao",aliases=["chengtts"])
    @asyncio.coroutine
    def cheng_tts(self, ctx):
        """Cheng generator read aloud :P\nThis command doesn't work in all channels."""
        cheng = (random.choice(copypastas["cheng_intro"])
                + random.choice(copypastas["cheng_middle"])
                + random.choice(copypastas["cheng_end"]))
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(cheng, tts=True)

    @commands.command(pass_context=True)
    @asyncio.coroutine
    def deward(self, ctx):
        """Deward RP quote generator\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(random.choice(copypastas["deward"]))

    @commands.command(pass_context=True,hidden=True,description="wait how the fuck did you find this lmao",aliases=["dewardtts"])
    @asyncio.coroutine
    def deward_tts(self, ctx):
        """deward RP quote generator read aloud :P\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(random.choice(copypastas["deward"]), tts=True)

    @commands.command(pass_context=True)
    @asyncio.coroutine
    def howard(self, ctx):
        """Howard RP quote generator\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(random.choice(copypastas["howard"]))

    @commands.command(pass_context=True,hidden=True,description="wait how the fuck did you find this lmao",aliases=["howardtts"])
    @asyncio.coroutine
    def howard_tts(self, ctx):
        """Howard RP quote generator read aloud :P\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(random.choice(copypastas["howard"]), tts=True)

    @commands.command(pass_context=True)
    @asyncio.coroutine
    def cah(self, ctx):
        """Cards against Humanity cue generator.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("``" + random.choice(copypastas["cues"]) + "``")

    @commands.command(pass_context=True,hidden=True,description="wait how the fuck did you find this lmao",aliases=["cahtts"])
    @asyncio.coroutine
    def cah_tts(self, ctx):
        """Howard RP quote generator read aloud :P\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(random.choice(copypastas["cues"]), tts=True)

    @commands.command(pass_context=True)
    @asyncio.coroutine
    def merio(self, ctx):
        """Merio's Journal.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(random.choice(copypastas["merio"]))

    @commands.command(pass_context=True,hidden=True,description="wait how the fuck did you find this lmao",aliases=["meriotts"])
    @asyncio.coroutine
    def merio_tts(self, ctx):
        """Merio's Journal read aloud :P\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(random.choice(copypastas["merio"]), tts=True)

    @commands.group(pass_context=True)
    @asyncio.coroutine
    def sloth(self, ctx):
        """Sloth quote generator\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            if ctx.invoked_subcommand is None:
                yield from self.bot.say(random.choice(copypastas["sloth"]))
    
    @sloth.command(pass_context=True)
    @asyncio.coroutine
    def original(self, ctx):
        """Sloth's original!\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(copypastas["sloth"][0])

    @commands.command(pass_context=True,hidden=True,description="wait how the fuck did you find this lmao",aliases=["slothtts"])
    @asyncio.coroutine
    def sloth_tts(self, ctx):
        """Sloth quote generator read aloud :P\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(random.choice(copypastas["sloth"]), tts=True)

    @commands.command(pass_context=True,aliases=["nomanssky","nomansky"])
    @asyncio.coroutine
    def nms(self, ctx):
        """THE ABSOLUTELY CRINGIEST COMMAND EVER\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(random.choice(copypastas["nms"]))

    @commands.command(pass_context=True,aliases=["minimacro"])
    @asyncio.coroutine
    def bs(self, ctx):
        """Just... try it ;^D\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("https://youtu.be/r427LYKA8zY")

    @commands.command(pass_context=True,hidden=True,description="wait how the fuck did you find this lmao",aliases=["nomanssky_tts","nomansky_tts","nomansskytts","nomanskytts","nmstts"])
    @asyncio.coroutine
    def nms_tts(self, ctx):
        """... If you like to hear verbally spoken cringe.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(random.choice(copypastas["nms"]), tts=True)

    @commands.command(pass_context=True,aliases=["dong","penis","cock"])
    @asyncio.coroutine
    def this(self, ctx, length: str = None):
        """Generates a text penis with a given length.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            if (length != None):
                this_string = this_gen(length)
                yield from self.bot.say(this_string)
            else:
                yield from self.bot.say("8================D")

    @commands.command(pass_context=True)
    @asyncio.coroutine
    def wow(self, ctx, number: str = None):
        """Generates an emphatic wow with a given length."""
        if (number != None):
            wow_string = wow_gen(number)
            yield from self.bot.say(wow_string)
        else:
            yield from self.bot.say("***__~~woooooooooooooooooooooooooooooow~~__***")

    @commands.command(pass_context=True, hidden = True)
    @asyncio.coroutine
    def fuck(self, ctx):
        """FUCK ON ME!!!!!!!!!!\nThis command only works in certain channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(fucc())

    @commands.command(pass_context=True, hidden = True,
        description='WARNING: THIS WILL DRIVE YOUR SERVER INSANE', aliases=["fucktts"])
    @asyncio.coroutine
    def fuck_tts(self, ctx):
        """FUCK ON ME!!!!!!!!!!\nThis command only works in certain channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(fucc())

    @commands.command(pass_context=True)
    @asyncio.coroutine
    def metal(self, ctx):
        """Generates text metal.\nThis command only works in certain channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say(metal())

    @commands.command(pass_context=True, hidden = True,
        description='WARNING: THIS WILL DRIVE YOUR SERVER INSANE', aliases=["metaltts"])
    @asyncio.coroutine
    def metal_tts(self, ctx):
        """Generates text metal.\nThis command only works in certain channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("**METAL!**", tts=True)
            yield from self.bot.say(metal_crazy_a(), tts=True)
            yield from self.bot.say("***AND NOW THE SOLO!!!***", tts=True)
            yield from self.bot.say("**___~~" + metal_crazy_b() + "~~___**", tts=True)

    @commands.command(pass_context=True, aliases=["add_shiptoast"])
    @checks.is_owner()
    @asyncio.coroutine
    def addshiptoast(self, ctx, channel: str = None):
        """Adds a channel name to the list of shiptoast channels.

        Without a channel specified, it will add the current channel."""
        sanitized = name_sanitize(channel)
        if sanitized is None:
            if ctx.message.channel.name in self.settings["shiptoast"]:
                yield from self.bot.say("This channel is already in the shiptoast list!")
                return
            else:
                channel_name = ctx.message.channel.name
        else:
            channel_name = sanitized
        self.settings["shiptoast"].append(channel_name)
        self.save_settings()
        yield from self.bot.say("Channel {} added.".format(channel_name))

    @commands.command(pass_context=True, aliases=["del_shiptoast"])
    @checks.is_owner()
    @asyncio.coroutine
    def delshiptoast(self, ctx, channel: str = None):
        """Removes a channel name from the list of shiptoast channels.

        Without a channel specified, it will remove the current channel."""
        sanitized = name_sanitize(channel)
        if sanitized is None:
            channel_name = ctx.message.channel.name
        else:
            channel_name = sanitized
        if channel_name in self.settings["shiptoast"]:
            self.settings["shiptoast"].remove(channel_name)
            self.save_settings()
            yield from self.bot.say("Channel {} removed.".format(channel_name))
        else:
            yield from self.bot.say("Channel {} not found in list.".format(channel_name))

    @commands.command(pass_context=True, aliases=['triple_a','aaa'])
    @asyncio.coroutine
    def trippleaaa(self, ctx):
        """TrippleAAA in a nutshell.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("https://cdn.discordapp.com/attachments/190191670304833536/201368263203094528/10a.png")

    @commands.command(pass_context=False, aliases=['mad'])
    @asyncio.coroutine
    def angry(self):
        """Displays an angry emoticon."""
        yield from self.bot.say("**___~~>:C~~___**")

    @commands.command(pass_context=True, aliases=['megadrive'], hidden = True)
    @asyncio.coroutine
    def genesis(self, ctx):
        """..."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("Why would someone initiate the genesis of such a horrid contraption?")

    @commands.command(pass_context=True, aliases=['love'])
    @asyncio.coroutine
    def hyena(self, ctx):
        """..."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("I have never kissed a girl. I have a tendency to lie awake at night and hope that someday that changes, but that would take a miracle. I wish I could go back in time and choose a different set of hobbies, but that probably is not going to happen. If it did, I would spend more time being active. I have a malformed body. I will probably die before my time because I liked to look at television sets and computer monitors instead of admiring the natural beauty of the outdoors. I want to wake up in my bed to the sound of a girl's breathing. I want to feel her body heat at my back. That's me.")

    @commands.command(pass_context=True)
    @asyncio.coroutine
    def clap(self, ctx):
        """Displays the Skype clap emote.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("https://i.imgur.com/3es8mZ6.gif")

    @commands.command(pass_context=True)
    @asyncio.coroutine
    def cry(self, ctx):
        """Displays the Skype crying emote.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("https://puu.sh/l3bnv.gif")

    @commands.command(pass_context=False,aliases=['kerathumbs'])
    @asyncio.coroutine
    def kfarathumbs(self):
        """Displays kfaraday's signature thumbs up."""
        yield from self.bot.say("( ¯u¯)-b")

    @commands.command(pass_context=False,aliases=['creepy','lewd'])
    @asyncio.coroutine
    def lenny(self):
        """Displays the lenny face."""
        yield from self.bot.say("( ͡° ͜ʖ ͡°)")

    @commands.command(pass_context=False,aliases=['snivvy','snivvi'])
    @asyncio.coroutine
    def snivi(self):
        """Displays the snivi face."""
        yield from self.bot.say("***__>;v__***")

    @commands.command(pass_context=False,aliases=['bear','pedobear'])
    @asyncio.coroutine
    def pedo(self):
        """Displays the pedobear face."""
        yield from self.bot.say("ʕ•͡ᴥ•ʔ")

    @commands.command(pass_context=True,aliases=['approve'])
    @asyncio.coroutine
    def seal(self, ctx):
        """Displays a seal of approval.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("https://cdn.discordapp.com/attachments/158305327035449344/159801148642033667/Joltik_Seal_of_Approval.png")

    @commands.command(pass_context=True,aliases=['asleep','assleap'])
    @asyncio.coroutine
    def sleep(self, ctx):
        """Displays a sleeping emote.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("https://cdn.discordapp.com/attachments/125591492004806656/207330607997386753/leap.gif")

    @commands.command(pass_context=True,aliases=['mogamen','humour'])
    @asyncio.coroutine
    def notfunny(self, ctx):
        """When something just ain't funny.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("https://cdn.discordapp.com/attachments/202817966570471426/219488871602192384/notfunny.png")

    @commands.command(pass_context=True,aliases=['somethinghappened','something_happened'])
    @asyncio.coroutine
    def something(self, ctx):
        """Something happened.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("https://cdn.discordapp.com/attachments/130833169724342272/202122586740490241/3dtq5QP.png")

    @commands.command(pass_context=True)
    @asyncio.coroutine
    def woody(self, ctx, woody_count: int = 9001):
        """Returns a random Woody picture hosted on dpc's website.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            if (woody_count < 1) or (woody_count > 3202):
                woody_count = randint(1,3201)
            if woody_count in [348, 475, 481, 530, 1492, 1549, 2500]:
                yield from self.bot.say("http://dpc.hol.es/woody/{}.gif".format(woody_count))
            else:
                yield from self.bot.say("http://dpc.hol.es/woody/{}.jpg".format(woody_count))

    @commands.command(pass_context=True,aliases=['cute'])
    @asyncio.coroutine
    def animal(self, ctx, animal_count: int = 9001):
        """Returns a random animal GIF hosted on dpc's website.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            if (animal_count < 1) or (animal_count > 104):
                animal_count = randint(1,104)
            yield from self.bot.say("http://dpc.hol.es/Animal/{}.gif".format(animal_count))
    
    @commands.command(pass_context=True,aliases=['disclaimer'])
    @asyncio.coroutine
    def gift(self, ctx):
        """Just... try it.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("https://www.mattandreko.com/images/brainpan2_preview.png")

    @commands.group(pass_context=True)
    @asyncio.coroutine
    def base64(self, ctx):
        """Base64 commands"""
        if ctx.invoked_subcommand is None:
            yield from self.bot.say('u idiot what did you expect me to do')

    @base64.command(pass_context=False)
    @asyncio.coroutine
    def encode(self, *, message):
        """Encodes Base64"""
        encoded = str(standard_b64encode(message.encode('utf-8')))
        if len(encoded) <= 1997:
            yield from self.bot.say("```~ " + encoded[2:len(encoded)-1] + "```")
        else:
            yield from self.bot.say("Sorry bud, but my encode won't fit in here. **_: )_**")

    @base64.command(pass_context=False)
    @asyncio.coroutine
    def decode(self, *, message):
        """Decodes Base64"""
        decoded = str(standard_b64decode(message))
        if len(decoded) <= 1999:
            yield from self.bot.say("```~ " + decoded[2:len(decoded)-1] + "```")
        else:
            yield from self.bot.say("Sorry bud, but my decode won't fit in here. **_: )_**")

    @asyncio.coroutine
    def on_message(self, message):
        if (message.author != self.bot.user) and (shiptoast_check(self, message)):
            if (message.content.lower().find("case in point") != -1):
                yield from self.bot.send_message(message.channel, '\uD83D\uDC49\uD83D\uDCBC point in case')
            elif (message.channel.id != "222432649472376832"):
                if ("cum" in message.content.lower().split()):
                    yield from self.bot.send_message(message.channel, 'oi mate watch your fuckin language')
                elif (message.content.lower().startswith('ok')):
                    yield from self.bot.send_message(message.channel, 'ok')
                elif (message.author.id == "125110486650847232"):
                    yield from self.bot.send_message(message.channel, 'hi liam')


def check_folders():
    folders = ["data/bulbacore"]
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    default = {"shiptoast": ['bot-playground', 'shitposting',
        'shiptoasting', 'bot-operation', 'bot-test-and-dev', 'playground',
        'botspam', 'breakfast-mondays', 'nicken-chugget', 'nsfw_jesus_christ',
        'hell', 'savespam','157614304059850752']}
    settings_path = "data/bulbacore/settings.json"

    if not os.path.isfile(settings_path):
        print("Creating default Bulbacore settings.json...")
        fileIO(settings_path, "save", default)
    else:  # consistency check
        current = fileIO(settings_path, "load")
        if current.keys() != default.keys():
            for key in default.keys():
                if key not in current.keys():
                    current[key] = default[key]
                    print(
                        "Adding " + str(key) + " field to Bulbacore settings.json")
            fileIO(settings_path, "save", current)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Bulbacore(bot))
