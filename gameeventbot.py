import os
import discord
from discord.ext import commands
import random
import asyncio
from collections import defaultdict, Counter
import time
import GameEvent


TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_reaction_remove(reaction, user):
    m_id = reaction.message.id
    if m_id in m_idToIdx.keys():
        eventDict[m_idToIdx[m_id]].remove_user(user)

@bot.event
async def on_reaction_add(reaction, user):
    m_id = reaction.message.id
    if m_id in m_idToIdx.keys():
        eventDict[m_idToIdx[m_id]].add_user(user)

@bot.command(name='summon')
async def poll(ctx, game, time: float, min_players: int = 0):
    idx = random.randint(100000,999999)
    while idx in eventDict.keys():
        idx = random.randint(100000,999999)
    
    hour_multiplier = 3600
    message = await ctx.send("react to play {} in {} hours \nmin_players {}\nid: {}".format(game, time, min_players, idx))
    m_id = message.id
    print(min_players)
    event = GameEvent.GameEvent(message.id, idx, ctx.author, time, min_players) 
    m_idToIdx[message.id] = idx
    eventDict[idx] = event 
    htime = int(time * hour_multiplier)
    await asyncio.sleep(htime)
    # TODO fix the check here 
    if idx in eventDict.keys():
        if eventDict[idx].valid:
            await notify(ctx, m_id)

@bot.command(name='cancel')
async def cancel_notif(ctx, idx: int):
    if idx in eventDict.keys():
        event = eventDict[idx]
        author = ctx.author
        override = False
        if str(author) == 'NAN#4085':
            override = True
        success = event.cancel(ctx.author, override)
        if success:
            await cleanup_event(event.m_id)
            await ctx.send("{} has been canceled".format(idx))
        else:
            await ctx.send("{} has not been canceled (not authorized)".format(idx))
    else:
        await ctx.send("{} is not a valid id".format(idx))

async def notify(ctx, m_id):
    valid = False
    if m_id in m_idToIdx.keys():
        event = eventDict[m_idToIdx[m_id]]
        if event.enough_people:
            valid = True
        else:
            await cleanup_event(m_id)
            valid = False
    else:
        valid = False

    if valid:
        event = eventDict[m_idToIdx[m_id]] 
        user_tags = " ".join([user.mention for user in event.get_users()])
        await ctx.send("It's Game Time! " + user_tags)
        await cleanup_event(m_id)

async def cleanup_event(m_id):
    idx = m_idToIdx[m_id]
    del m_idToIdx[m_id]
    del eventDict[idx]

if __name__ == "__main__":
    m_idToIdx = {}
    eventDict = {}
    bot.run(TOKEN)
