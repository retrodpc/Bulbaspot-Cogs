import asyncio
from random import randint
import random
import json
import os

from discord.ext import commands

from __main__ import send_cmd_help
from cogs.utils.dataIO import fileIO


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
    folders = ["data/saveybot"]
    for folder in folders:
        if not os.path.exists(folder):
            print("Creating " + folder + " folder...")
            os.makedirs(folder)


def check_files():
    default = [{"slot": "0", "name": "Bulbasalt", "message": "lol self-insert xddd"}]
    settings_path = "data/saveybot/saveybot.json"

    if not os.path.isfile(settings_path):
        print("Creating default saveybot.json...")
        fileIO(settings_path, "save", default)


# idk why i need this here but ahhh well -_-
check_folders()
check_files()


with open('data/saveybot/saveybot.json','r') as saveybot_file:    
    save_data = json.load(saveybot_file)


def save(data):
    with open('data/saveybot/saveybot.json',"w") as saveybot_file:
        json.dump(data, saveybot_file, indent=4) 


@asyncio.coroutine
def lowest_available():
    save_list = []
    for save_state in save_data:
        save_slot = save_data[save_data.index(save_state)]["slot"]
        if (int(save_slot) > 0):
            save_list.append(int(save_slot)) # has to be int in order to sort; str will sort alphabetical
    save_list.sort()
    unavailable = True
    loop_count = 0
    while unavailable:
        if save_list[loop_count] != loop_count + 1:
            unavailable = False
            return str(loop_count + 1)
        loop_count += 1


@asyncio.coroutine
def slot_index(slot: str):
    save_list = []
    for save_state in save_data:
        save_slot = save_data[save_data.index(save_state)]["slot"]
        save_list.append(save_slot)
    if slot in save_list:
        return save_list.index(slot)
    else:
        raise "Savestate does not exist!"


#def fetch_all_slots():
    #slots = []
    #for save_state in save_data:
        #save_content = save_data[save_data.index(save_state)]["slot"]
        #save_list.append(save_content)
    #return content


@asyncio.coroutine
def fetch_all_content():  # returns the content of every goddamned save ever
    content = []
    for save_state in save_data:
        save_content = save_data[save_data.index(save_state)]["message"]
        content.append(save_content)
    return content


@asyncio.coroutine
def fetch_content(slots: list):  # returns an array full of saves that match the given slots
    content = []
    for slot in slots:
        slot_index = yield from slot_index(slot)
        save_content = save_data[slot_index]["message"]
        content.append(save_content)
    return content


@asyncio.coroutine
def search_content(search: str):  # returns an array full of slots that contain the search query
    slots = []
    for save_state in save_data:
        save_content = save_data[save_data.index(save_state)]["message"]
        save_slot = save_data[save_data.index(save_state)]["slot"]
        if search.lower() in save_content.lower():
            slots.append(save_slot)
    return slots


@asyncio.coroutine
def array_word_split(array: list):  # splits strings inside lists
    split_array = []
    for element in array:
        split_element = element.split()
        for word in split_element:
            split_array.append(word)
    return split_array


@asyncio.coroutine
def owner(owner: str, **kwargs):  # using name as well as id to maintain compatibility with irc savestates
    save_list = []
    owner_id = kwargs.get('owner_id', None)
    for save_state in save_data:
        save_slot = save_data[save_data.index(save_state)]["slot"]
        save_author = save_data[save_data.index(save_state)]["name"]
        if (save_author.lower() == owner.lower()):
            save_list.append(save_slot)
    if owner_id is not None:
        for save_state in save_data:
            try:
                saver_id = save_data[save_data.index(save_state)]["saver_id"]
                save_slot = save_data[save_data.index(save_state)]["slot"]
                if (saver_id == owner_id):
                    save_list.append(save_slot)
            except:
                pass

    output_list = []  # removing inevitable duplicates
    seen = set()
    for value in save_list:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output_list.append(value)
            seen.add(value)

    return output_list


@asyncio.coroutine
def get_random(array: list, count: int):
    random_array = []
    for i in range(0,count):
        random_array.append(random.choice(array))
    return random_array


class SaveyBot:
    """Lets you save and load your personal picture & bio.\n(oh this is a prototype for saveybot-like functionality)\n"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, aliases=["savey", "savestate", "s"], no_pm=True)
    @asyncio.coroutine
    def saveybot(self, ctx):
        """Lets you save and load states, a la SaveyBot."""
        if ctx.invoked_subcommand is None:
            yield from send_cmd_help(ctx)

    @saveybot.command(pass_context=True)
    @asyncio.coroutine
    def save(self, ctx, *, params: str = None):
        """Saves a savestate. It's yours to keep.\nYou can specify the slot as the first argument if you want.\n\n?saveybot save <message>\n?saveybot save <slot> <message>"""
        args = params.split()
        if params is None:
            yield from self.bot.say("~ what did he mean by this?")
            return
        elif (is_int(args[0]) and (len(args) > 1)):  # separates slot from commands
            slot = str(args[0])
            content = params[len(args[0]):]
        else:
            slot = yield from lowest_available()
            content = params

        if len(content) > 1900:
            yield from self.bot.say("~ woah chill you're trying to save too much")
            return

        try:  # seeing if the savestate exists
            data_index = yield from slot_index(slot)
        except Exception:
            if is_int(slot):
                save_data.append({"name": ctx.message.author.name, "slot": slot, "message": content, "saver_id": ctx.message.author.id})
                save(save_data)
                yield from self.bot.say("~ new state ``{0}`` saved!".format(slot))
            else:
                yield from self.bot.say("~ u n00b that's not a number")
            return

        try:  # seeing if the savestate has an author.id saved
            saver_id = save_data[data_index]["saver_id"]
        except:
            saver_id = "Unknown"

        if (ctx.message.author.id == saver_id):
            save_data[data_index] = ({"name": ctx.message.author.name, "slot": slot, "message": content, "saver_id": ctx.message.author.id})
            save(save_data)
            yield from self.bot.say('~ state ``{0}`` saved!'.format(slot))
        elif ("Unknown" == saver_id):
            yield from self.bot.say("~ woah there buddy, state ``{0}`` came from irc and it's staying around, ya hear?".format(slot))
        else:
            yield from self.bot.say("~ wtf did You try to overwrite state ``{0}``??? that's not Yours ***__~~>:C~~__***".format(slot))

    @saveybot.command(pass_context=False, aliases=["available","lowest"])
    @asyncio.coroutine
    def low(self):
        """Lowest available savestate."""
        lowest = yield from lowest_available()
        yield from self.bot.say("~ lowest savestate available is {0} :D/".format(lowest))

    @saveybot.command(pass_context=True, aliases=["delet","delete"])
    @asyncio.coroutine
    def remove(self, ctx, slot: str):
        """Removes your savestate."""
        try: #seeing if the savestate exists
            data_index = yield from slot_index(slot)
        except Exception:
            if is_int(slot):
                yield from self.bot.say("~ the savestate doesn't exist! (you should make it!!!!)")
            else:
                yield from self.bot.say("~ u n00b that's not a number")
            return

        try: #seeing if the savestate has an author.id saved
            saver_id = save_data[data_index]["saver_id"]
        except:
            saver_id = "Unknown"

        if (ctx.message.author.id == saver_id):
            del save_data[data_index]
            save(save_data)
            yield from self.bot.say('~ state ``{0}`` removed!'.format(slot))
        elif ("Unknown" == saver_id):
            yield from self.bot.say("~ woah there buddy, state ``{0}`` came from irc and it's staying around, ya hear?".format(slot))
        else:
            yield from self.bot.say("~ wtf did You try to remove state ``{0}``??? that's not Yours ***__~~>:C~~__***".format(slot))

    @saveybot.command(pass_context=False)
    @asyncio.coroutine
    def load(self, slot: str):
        """Loads a single savestate.\nFor the SaveyBot command that lets you load a user's savestates, do ?saveybot loaduser <user>."""
        try: #seeing if the savestate exists
            data_index = yield from slot_index(slot)
        except Exception:
            if is_int(slot):
                yield from self.bot.say("~ the savestate doesn't exist! (you should make it!!!!)")
            else:
                yield from self.bot.say("~ u n00b that's not a number")
            return

        state_content = save_data[data_index]["message"]
        yield from self.bot.say('~ {0}'.format(state_content))

    @saveybot.command(pass_context=True, aliases=["randomload","random_load"])
    @asyncio.coroutine
    def road(self, ctx, user: str = None):
        """Loads a random savestate.\nUser can be specified in the future."""
        if user is not None: # temp fix
            user = None
            yield from self.bot.say("~ user-specific randomload is disabled until coding is fixed")

        if user is None:
            random_index = randint(0,len(save_data)-1)
            state_content = save_data[random_index]["message"]
            state_slot = save_data[random_index]["slot"]
            state_author = save_data[random_index]["name"]
            yield from self.bot.say('~ {1} ({2}): {0}'.format(state_content, state_slot, state_author))

        else:
            user_object = ctx.message.server.get_member_named(user) # handles username and userid
            if user_object is None:
                user_name = user
                user_id = None
            else:
                user_name = user_object.name
                user_id = user_object.id
            slots = yield from owner(user_name, owner_id=user_id)

            random_slot = slots[randint(0,len(slots)-1)]
            random_slot_index = yield from slot_index(random_slot)
            state_content = save_data[random_slot_index]["message"]
            state_slot = random_slot
            state_author = save_data[random_slot_index]["name"]
            yield from self.bot.say('~ {1} ({2}): {0}'.format(state_content, state_slot, state_author))

    @saveybot.command(pass_context=False)
    @asyncio.coroutine
    def json(self):
        """Posts a link to the bot's database."""
        yield from self.bot.say('~ https://botb.club/~dpc/saveybot.json')

    @saveybot.command(pass_context=False)
    @asyncio.coroutine
    def whois(self, slot: str):
        """Gets a savestate's author."""
        try: #seeing if the savestate exists
            data_index = yield from slot_index(slot)
        except Exception:
            if is_int(slot):
                yield from self.bot.say("~ the savestate doesn't exist! (you should make it!!!!)")
            else:
                yield from self.bot.say("~ u n00b that's not a number")
            return

        state_author = save_data[data_index]["name"]
        yield from self.bot.say('~ slot ``{0}`` is owned by ``{1}``.'.format(slot, state_author))

    @saveybot.command(pass_context=True)
    @asyncio.coroutine
    def search(self, ctx, *, search: str):
        """Queries the database for the search."""
        search_slots = yield from search_content(search)  # query
        if len(search_slots) > 0:
            output = "~ matches for ``{0}``: {1}".format(search, ", ".join(search_slots))
            if (len(output) <= 2000):
                yield from self.bot.say(output)
            else:
                filename = '{0}-search.txt'.format(search.lower().replace(' ', '_'))
                with open("data/saveybot/" + filename, "w") as output_file:
                    output_file.write(output)
                with open("data/saveybot/" + filename, "r") as output_file:
                    yield from self.bot.send_file(ctx.message.channel, output_file)
        else:
            yield from self.bot.say("no matches for {0} :(".format(search))

    @saveybot.command(pass_context=True)
    @asyncio.coroutine
    def loaduser(self, ctx, *, user: str):
        """Lists all the saves that this user owns."""
        user_object = ctx.message.server.get_member_named(user)  # handles username and userid
        if user_object is None:
            user_name = user
            user_id = None
        else:
            user_name = user_object.name
            user_id = user_object.id

        saves = yield from owner(user_name, owner_id=user_id)
        if len(saves) > 0:
            output = "~ {0} owns savestates: {1}".format(user_name, ", ".join(saves))
            if (len(output) <= 2000):
                yield from self.bot.say(output)
            else:
                filename = '{0}-saves.txt'.format(user_name.lower().replace(' ', '_'))
                with open("data/saveybot/" + filename, "w") as output_file:
                    output_file.write(output)
                with open("data/saveybot/" + filename, "r") as output_file:
                    yield from self.bot.send_file(ctx.message.channel, output_file)
        else:
            yield from self.bot.say("~ this user owns no savestates =(")

    @saveybot.command(pass_context=True, aliases=["markof"])
    @asyncio.coroutine
    def markov(self, ctx, *args):
        """Takes random words from savestates.\nmarkov for users is disabled and will act the same as global markov.\n\n?saveybot markov\n?saveybot markov <user>\n?saveybot markov <count>\n?saveybot markov <user> <count>"""
        if (len(args) < 1):
            count = 10
            user = None
        elif is_int(args[0]):
            count = int(args[0])
            if count > 50:
                count = 50
            elif count < 1:
                count = 1
            user = None
        elif (len(args) > 1) and is_int(args[1]):
            count = int(args[1])
            if count > 50:
                count = 50
            elif count < 1:
                count = 1
            user = str(args[0])
        else:
            count = 10
            user = str(args[0])

        if user is not None:  # placeholder until i can fix it
            user = None
            yield from self.bot.say("~ user-specific markov is disabled until coding is fixed")

        if user is None:
            all_content = yield from fetch_all_content()
            all_words = yield from array_word_split(all_content)
            random_words = yield from get_random(all_words, count)
            content = ' '.join(random_words)
            if len(content) > 1998:
                content = content[:1998]
            yield from self.bot.say("~ " + content)
        else:
            user_object = ctx.message.server.get_member_named(user)  # handles username and userid
            if user_object is None:
                user_name = user
                user_id = None
            else:
                user_name = user_object.name
                user_id = user_object.id

            slots = yield from owner(user_name, owner_id=user_id)
            slots_content = yield from fetch_content(slots)
            all_words = yield from array_word_split(slots_content)
            random_words = yield from get_random(all_words, 10)
            content = ' '.join(random_words)
            if len(content) > 1998:
                content = content[:1998]
            yield from self.bot.say("~ " + content)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(SaveyBot(bot))
