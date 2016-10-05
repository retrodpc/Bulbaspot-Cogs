import asyncio
import json

from discord.ext import commands


with open('data/pix/pix.json') as pix_file:
    pixies = json.load(pix_file)


def save(data):
    with open('data/pix/pix.json', "w") as pix_file:
        json.dump(data, pix_file, indent=4)


class Pix:
    """Lets you save and load your personal profile.\n(oh this is a prototype for saveybot-like functionality)\n"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, no_pm=True, aliases=["profile", "pic"])
    @asyncio.coroutine
    def pix(self, ctx):
        """Lets you save and load your personal profile."""
        if ctx.invoked_subcommand is None:
            yield from self.bot.say('Invalid subcommand. Type ``?help pix`` for proper usage.')

    @pix.command(pass_context=True, no_pm=True)
    @asyncio.coroutine
    def save(self, ctx, *, message):
        """Saves your personal profile on this server.\nThere is no data validation. __You__ are responsible for making sure that the content is cromulent."""
        if (ctx.message.server.id in pixies["server"]):
            if (ctx.message.author.id in pixies["server"][ctx.message.server.id]["user"]):
                data_index = pixies["server"][ctx.message.server.id]["user"].index(ctx.message.author.id)
                pixies["server"][ctx.message.server.id]["content"][data_index] = message
                ctx.message.server.id
                save(pixies)
                yield from self.bot.say('Picture saved.')
            else:
                pixies["server"][ctx.message.server.id]["user"].append(ctx.message.author.id)
                pixies["server"][ctx.message.server.id]["content"].append(message)
                save(pixies)
                yield from self.bot.say('Picture saved.')
        else:
            pixies["server"][ctx.message.server.id] = {"user": [], "content": []}
            pixies["server"][ctx.message.server.id]["user"].append(ctx.message.author.id)
            pixies["server"][ctx.message.server.id]["content"].append(message)
            save(pixies)
            yield from self.bot.say('Picture saved.')

    @pix.command(pass_context=True, no_pm=True)
    @asyncio.coroutine
    def remove(self, ctx):
        """Removes your personal profile from this server."""
        if (ctx.message.author.id in pixies["server"][ctx.message.server.id]["user"]):
            data_index = pixies["server"][ctx.message.server.id]["user"].index(ctx.message.author.id)
            del pixies["server"][ctx.message.server.id]["user"][data_index]
            del pixies["server"][ctx.message.server.id]["content"][data_index]
            save(pixies)
            yield from self.bot.say('Picture removed.')
        else:
            yield from self.bot.say("You can't remove something that doesn't exist!")

    @pix.command(pass_context=True, no_pm=True)
    @asyncio.coroutine
    def load(self, ctx, *, user: str = None):
        """Loads a personal profile from this server & bio."""
        if (ctx.message.server.id in pixies["server"]):
            if (user is None):
                user_object = ctx.message.author
            elif (len(ctx.message.mentions) == 1):
                user_object = ctx.message.mentions[0]
            elif (len(ctx.message.mentions) > 1):
                yield from self.bot.say('One person at a time please!')
                return
            else:
                user_object = ctx.message.server.get_member_named(user)
            if (user_object is None):
                yield from self.bot.say('User not found.')
            elif (user_object.id in pixies["server"][ctx.message.server.id]["user"]):
                data_index = pixies["server"][ctx.message.server.id]["user"].index(user_object.id)
                yield from self.bot.say("``Loading profile of " + user_object.name + "...``\n\n" + pixies["server"][ctx.message.server.id]["content"][data_index])
            else:
                yield from self.bot.say('This user has no picture saved.')


def setup(bot):
    bot.add_cog(Pix(bot))
