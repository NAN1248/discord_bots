import os
import discord
from discord.ext import commands
# from dotenv import load_dotenv
import random
import asyncio
from collections import defaultdict, Counter
#import sched
import time

# load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')
# TODO Add event class to store instead of these globals
bot = commands.Bot(command_prefix='!')

message_dict = defaultdict(Counter)
idx_to_message = {}
#s = sched.scheduler(time.time, time.sleep)


@bot.event
async def on_reaction_remove(reaction, user):
    global message_dict
    m_id = reaction.message.id
    if message_dict[m_id][user] == 1:
        del message_dict[m_id]
    else:
        message_dict[m_id][user] -= 1

@bot.event
async def on_reaction_add(reaction, user):
    global message_dict
    if reaction.message.author.name == 'GameSummonBot':
        # user_list.append("@"+str(user.id))
        m_id = reaction.message.id
        if await is_valid_summon(m_id):
            message_dict[reaction.message.id][user] += 1

        # user_list.append(user.mention)


@bot.command(name='summon')
async def poll(ctx, game, time: float, min_players: int = 0):
    global message_dict
    global idx_to_message
    idx = random.randint(100000,999999)
    hour_multiplier = 3600

    message = await ctx.send("react to play {} in {} hours \nmin_players {}\nid: {}".format(game, time, min_players, idx))
    idx_to_message[idx] = message
    #s.enter()
    # todo: Make canceling less garbage
    htime = int(time * hour_multiplier)
    print("entered waiting for {} seconds ".format(htime))
    await asyncio.sleep(htime)
    print('finsihed sleep')
    await notify(ctx, message.id)

@bot.command(name='cancel')
async def cancel_notif(ctx, idx: int):
    global message_dict
    global idx_to_message
    
    if idx not in idx_to_message.keys():
        await ctx.send("{} is not a valid id".format(idx))

    else:
        message = idx_to_message[idx]
        # await bot.delete_message(message)
        try:
            del message_dict[message.id]
        except KeyError:
            pass

        del idx_to_message[idx]
        await ctx.send("{} has been canceled".format(idx))


async def notify(ctx, m_id):
    global message_dict
    global idx_to_message
    
    if not await is_valid_summon(m_id):
        return

    user_set = message_dict[m_id].keys()
    user_tags = " ".join([user.mention for user in user_set])
    print("in notify")
    await ctx.send("It's Game Time! " + user_tags)
    for key, val in zip(idx_to_message.keys(), idx_to_message.values()):
        if val.id == m_id:
            del idx_to_message[key]
            break
    del message_dict[m_id]

async def is_valid_summon(m_id):
    global idx_to_message

    print("is_valid {}".format(m_id))
    valid_mids = set()
    for m in idx_to_message.values():
        valid_mids.add(m.id)

    if m_id not in valid_mids:
        print("invalid")
        del valid_mids
        return False
    del valid_mids
    return True

if __name__ == "__main__":
    bot.run(TOKEN)
'''
@bot.command(name='summon')
async def poll(ctx, game, time: int):
    global message_dict
    message = await ctx.send("react to play {} in {}".format(game, time))

    await asyncio.sleep(time)
    # check all users who reacted
    
    #for user in user_list:
    #    await bot.send_message(user, "It's Game Time")

    #user_tags = " ".join(user_list)
    #user_list = list()
    m_id = message.id
    user_set = message_dict[m_id].keys()
    user_tags = " ".join([user.mention for user in user_set])
    
    await ctx.send("It's Game Time! " + user_tags)
    del message_dict[m_id]
    # reaction = await bot.wait_for_reaction(emoji="💯", message=message)
    # await ctx.send(reaction.message.author)
@bot.command(name='99')
async def b99(ctx):

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]
    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)
'''

#async def notify(message)



