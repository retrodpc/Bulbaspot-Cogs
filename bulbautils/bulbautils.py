# Adds core commands formerly from Bulbaspot. This adds utility commands.
# LICENSE: This module is licenced under Apache License 2.0
# @category   Tools
# @copyright  Copyright (c) 2018 dpc
# @version    1.1
# @author     dpc

import asyncio

from discord.ext import commands


def decToHex(dec):
    hexDigits = "0123456789ABCDEF"
    conversion = ''	# (Re-)initiate string
    # dec referenced as division

    while dec != 0:
        remainder = dec % 16
        dec = dec // 16
        conversion += hexDigits[remainder]
    conversion = reverseString(conversion)

    return conversion


def reverseString(string):
    string = str(string)
    return string[::-1]


def calcDeltaHex(n, rate):	# n = semitone difference, rate = the initial samplerate of your sample in Hz
    a = 2**(1/12)		# a = 12-tones in an octave (see 'Frequency Table formula' for the 'equal tempered scale')
    fn = rate * (a**n)		# Calculates the freq of the note, in 'n' semitones away from original pitch

    delta = fn / (31250/255)		# 255 is FF in hex; the max value of 20xx
    delta = int(round(delta, 0))	# Rounds the delta value to 0 decimals
    return decToHex(delta)		# Converts delta value from decimal to hex


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Bulbautils:
    """Ivysalt's utility commands. Useful for chiptune stuff mostly."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=False, description='Calculates AddMusicK speed based on a tempo. Also gives a rounded speed and tempo if given tempo results in a non-integer speed.')
    @asyncio.coroutine
    def amkspeed(self, tempo: float):
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
                yield from self.bot.say("The AMK speed is about {:.0f}. The yielded tempo is {:g} BPM.".format(int(round(amkspeed)), round(amkspeed) * 625 / 256))
            else:
                yield from self.bot.say("The AMK speed is {:.0f}.".format(amkspeed))
        except ValueError as err:
            # Display error message to channel
            yield from self.bot.say("{} Type ``?help amkspeed`` for proper usage.".format(err))

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
            yield from self.bot.say("{} Type ``?help clockspeed`` for proper usage.".format(err))

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
            yield from self.bot.say("{} Type ``?help tickspeed`` for proper usage.".format(err))

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
            yield from self.bot.say("{} Type ``?help celsius`` for proper usage.".format(err))

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
            yield from self.bot.say("{} Type ``?help fahrenheit`` for proper usage.".format(err))

    @commands.command(pass_context=True, no_pm=False)
    @asyncio.coroutine
    def deltapcm(self, ctx, semitone_change: int=0, rate: float=31250.0):
        """Deflemask SegaPCM Delta Calculator."""
        if (semitone_change == 0 and rate == 31250.0):
            yield from self.bot.say("Type ``?help deltapcm`` to get usage information.")
            return
        elif (rate <= 0 or rate > 31250):
            yield from self.bot.say("Sample rate needs to be between 1 Hz and 31250 Hz... Type ``?help deltapcm`` to get usage information.")
        
        try:
            convertedHex = calcDeltaHex(semitone_change, rate)
        except OverflowError as err:
            yield from self.bot.say("{} Type ``?help deltapcm`` for proper usage.".format(err))
        
        if (convertedHex == ""):		# Check if hex value smaller than 00 or over FF and report to user
            yield from self.bot.say("ERROR: Underflow ! Type ``?help deltapcm`` to get usage information.")
        elif (len(convertedHex) > 2):    
            yield from self.bot.say("ERROR: Overflow ! Type ``?help deltapcm`` to get usage information.")
        else:
            if (len(convertedHex) == 1):    # Check if value not less than 10 (in hex) and add 0 if so
                convertedHex += "0"
                convertedHex = reverseString(convertedHex)
            yield from self.bot.say("Your delta command is: ``20{}``".format(convertedHex))


def setup(bot):
    bot.add_cog(Bulbautils(bot))