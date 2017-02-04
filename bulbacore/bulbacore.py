import asyncio
import random
from random import randint
from math import floor
from base64 import *
import json
import os
from string import ascii_letters, digits

from discord.ext import commands

from __main__ import send_cmd_help, settings
from cogs.utils import checks
from cogs.utils.dataIO import fileIO


def save_logs(filename, data):
    full_path = Path('data/logger/invoked_logs/' + filename)
    if full_path.is_file():
        with open(str(full_path), "ab") as log_file:
            log_file.write(data.encode("utf8"))
    else:
        with open(str(full_path), "wb") as log_file:
            log_file.write(data.encode("utf8"))


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


def is_float(s):
    try:
        float(s)
    except ValueError:
        return False
    return True


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
            for j in range(top_kek-1):
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
            for i in range(length):
                this_thing = this_thing + "="
            this_thing = this_thing + "D"
            return this_thing
        elif (length >= -1998 and length < 0):
            new_length = -length
            this_thing = "D"
            for i in range(new_length):
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
            for i in range(length):
                wow_thing = wow_thing + "o"
            wow_thing = wow_thing + "w~~__***"
            return wow_thing
        elif (length >= -1984 and length < 0):
            new_length = -length
            wow_thing = "***__~~ʍ"
            for i in range(new_length):
                wow_thing = wow_thing + "o"
            wow_thing = wow_thing + "ʍ~~__***"
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
    for i in range(metal_length):
        if randint(0, 9) < 9:
            metal_crusher = metal_crusher + primary_metal_chara[randint(0, len(primary_metal_chara)-1)]
        else:
            metal_crusher = metal_crusher + secondary_metal_chara[randint(0, len(secondary_metal_chara)-1)]
    for i in range(solo_length):
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
    for i in range(metal_length):
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
    for i in range(solo_length):
        if randint(0, 19) < 19:
            han_solo = han_solo + primary_solo_frisk[randint(0, len(primary_solo_frisk)-1)]
        else:
            han_solo = han_solo + secondary_solo_frisk[randint(0, len(secondary_solo_frisk)-1)]
    return han_solo


class Bulbacore:
    """Bulbasalt's commands ported over from the old Bulbaspot. Please don't abuse."""

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
    def woody(self, ctx, woody_count: int = randint(1,3201)):
        """Returns a random Woody picture hosted on dpc's website.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            if (woody_count < 0) or (woody_count > 3202):
                woody_count = = randint(1,3201)
            if woody_count in [348, 475, 481, 530, 1492, 1549, 2500]:
                yield from self.bot.say("http://dpc.hol.es/woody/{}.gif".format(woody_count))
            else:
                yield from self.bot.say("http://dpc.hol.es/woody/{}.jpg".format(woody_count))
    
    @commands.command(pass_context=True,aliases=['disclaimer'])
    @asyncio.coroutine
    def gift(self, ctx):
        """Just... try it.\nThis command doesn't work in all channels."""
        if (shiptoast_check(self, ctx.message)):
            yield from self.bot.say("https://www.mattandreko.com/images/brainpan2_preview.png")

    # Parse !amkspeed verbiage
    @commands.command(pass_context=False, description='Calculates AddMusicK speed based on a tempo. Also gives a rounded speed and tempo if given tempo results in a non-integer speed.')
    @asyncio.coroutine
    def amkspeed(self, tempo):
        """Calculates AddMusicK speed based on a tempo"""
        try:
            if (not is_float(tempo)):
                raise ValueError("Nice Number !")
            tempo = float(tempo)
            if (tempo <= 0):
                raise ValueError("Error: Tempo must be positive.")
            amkspeed = tempo * 256 / 625
            amkspeedtest = amkspeed % 1
            if (amkspeedtest != 0):
                amkspeedrounded = int(round(amkspeed))
                amktempo = float(amkspeedrounded) * 625 / 256
                yield from self.bot.say("The AMK speed is about {:.0f}. The yielded tempo is {:g} BPM.".format(amkspeedrounded, amktempo))
            else:
                yield from self.bot.say("The AMK speed is {:.0f}.".format(amkspeed))
        except ValueError as err:
            # Display error message to channel
            yield from self.bot.say(err)

    # Parse !clockspeed verbiage
    @commands.command(pass_context=False, description='Calculates clock speed based on first the desired tempo and then the tick speed.')
    @asyncio.coroutine
    def clockspeed(self, tempo, speed):
        """Calculates clock speed"""
        try:
            if (not is_float(tempo)):
                raise ValueError("Nice Numbers !")
            if (not is_float(speed)):
                raise ValueError("Nice Numbers !")
            tempo = float(tempo)
            speed = float(speed)
            if (tempo <= 0):
                raise ValueError("Error: Tempo must be positive.")
            if (speed <= 0):
                raise ValueError("Error: Tick speed must be positive.")
            constant = 15 / speed
            clockspeed = tempo / constant
            yield from self.bot.say("The clock speed is {:g} Hz.".format(clockspeed))
        except ValueError as err:
            # Display error message to channel
            yield from self.bot.say(err)

    # Parse !tickspeed verbiage
    @commands.command(pass_context=False, description='Calculates tick speed based on first the desired tempo and then the clock speed.')
    @asyncio.coroutine
    def tickspeed(self, tempo, clock):
        """Calculates tick speed"""
        try:
            if (not is_float(tempo)):
                raise ValueError("Nice Numbers !")
            if (not is_float(clock)):
                raise ValueError("Nice Numbers !")
            tempo = float(tempo)
            clock = float(clock)
            if (tempo <= 0):
                raise ValueError("Error: Tempo must be positive.")
            if (tempo <= 0):
                raise ValueError("Error: Clock speed must be positive.")
            tickspeed = 15 * clock / tempo
            # if the tickspeed is non-int it'll print past the period
            yield from self.bot.say("The tick speed is {:g}.".format(tickspeed))
        except ValueError as err:
            # Display error message to channel
            yield from self.bot.say(err)

    # Parse !celsius verbiage
    @commands.command(pass_context=False, description='Converts to Celsius from Fahrenheit.')
    @asyncio.coroutine
    def celsius(self, fahrenheit):
        """Converts to Celsius from Fahrenheit"""
        try:
            if (not is_float(fahrenheit)):
                raise ValueError("Nice Number !")
            fahrenheit = float(fahrenheit)
            celsius = (fahrenheit - 32) * (5 / 9)
            yield from self.bot.say("{:g}°F is {:g}°C.".format(fahrenheit, celsius))
        except ValueError as err:
            # Display error message to channel
            yield from self.bot.say(err)

    # Parse !fahrenheit verbiage
    @commands.command(pass_context=False, description='Converts to Fahrenheit from Celsius.')
    @asyncio.coroutine
    def fahrenheit(self, celsius):
        """Converts to Fahrenheit from Celsius"""
        try:
            if (not is_float(celsius)):
                raise ValueError("Nice Number !")
            celsius = float(celsius)
            fahrenheit = celsius * (9 / 5) + 32
            yield from self.bot.say("{:g}°C is {:g}°F.".format(celsius, fahrenheit))
        except ValueError as err:
            # Display error message to channel
            yield from self.bot.say(err)

    @commands.group(pass_context=True)
    @asyncio.coroutine
    def base64(self, ctx):
        """Base64 commands"""
        if ctx.invoked_subcommand is None:
            yield from send_cmd_help(ctx)
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

    @commands.command(pass_context=True, no_pm=True, aliases=["loglast"])
    async def log_last(self, ctx, messages: int = 100):
        """Logs previous messages in a channel.\nDefaults to 100 messages but has no limit."""
        await self.bot.say("Starting logging...")

        filename = 'log-{6}-{7}-{0:04d}{1:02d}{2:02d}-{3:02d}-{4:02d}-{5:02d}.log'.format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, ctx.message.server.name, ctx.message.channel.name)
        save_logs(filename, "Log started by {6} on {0:04d}/{1:02d}/{2:02d} at {3:02d}:{4:02d}:{5:02d} in channel {7} on server {8}, for no reason other than to piss Bulbasaur off.\nUser ID: {9}\nChannel ID: {10}\nServer ID: {11}\n".format(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, datetime.now().second, str(ctx.message.author), str(ctx.message.channel), str(ctx.message.server), ctx.message.author.id, ctx.message.channel.id, ctx.message.server.id))
        
        async for message in self.bot.logs_from(ctx.message.channel, messages):
            save_logs(filename, "[{0:04d}/{1:02d}/{2:02d}-{3:02d}:{4:02d}:{5:02d}] <{6}> {7}\n".format(message.timestamp.year, message.timestamp.month, message.timestamp.day, message.timestamp.hour, message.timestamp.minute, message.timestamp.second, message.author.name.encode('ascii', 'backslashreplace').decode('ascii'), message.content.encode('ascii', 'backslashreplace').decode('ascii')))
        
        with open("data/logger/invoked_logs/"+filename,"rb") as f_in, gzip.open("data/logger/invoked_logs/"+filename+'.gz', 'wb') as f_out:
            f_out.writelines(f_in)
        
        with open("data/logger/invoked_logs/"+filename+".gz","rb") as f_out:
            await self.bot.send_file(ctx.message.channel, f_out, content="Bulbasaur is going to be pissed at you.")

    #@asyncio.coroutine
    #def on_message(self, message):
        #if (message.content.lower().startswith('ok')
        #and (shiptoast_check(self, message))
        #and (message.author != self.bot.user)):
            #yield from self.bot.send_message(message.channel, 'ok')


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
