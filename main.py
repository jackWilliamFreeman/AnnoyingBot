import discord
import os
import random
from keep_alive import keep_alive


def is_int(value):
    try:
        int(value)
        return True
    except:
        return False


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

globalFactory = .1

def set_starter_threshold():
    global globalFactor
    globalFactor = .1


@client.event
async def on_message(message):
    annoyance_threshold = random.uniform(0, 1)

    if message.author == client.user:
        return

    if message.content.startswith('$annoyingbot'):
        global globalFactor
        globalFactor = await handle_annoyingbot_commands(message, globalFactor)

    if message.author.id == 550616372120387585 and annoyance_threshold <= globalFactor:
        print('annoying target')
        await message.channel.send('Ian you smell')

    if message.author.id == 752655419486371982:
        print('Encouraging Drinking')
        await message.channel.send('Ignore Drunkbot, drunk you is a better you')


async def handle_annoyingbot_commands(message, threshold):
    message_content = message.content
    if message_content.lower() == '$annoyingbot -help':
        await message.channel.send('Options:\n'
                                   '-hello annoyingBot will say hello\n'
                                   '-help gives you options\n'
                                   '-threshold -int sets threshold for activation based on int ie. 50 = 50%')
    if message_content.lower() == '$annoyingbot -hello':
        await message.channel.send('sup carnt?')
    if message_content.lower().startswith('$annoyingbot -threshold'):
        threshold = await set_threshold(message, message_content, threshold)
    if message_content.lower() == '$annoyingbot':
        await message.channel.send('give me some real instructions you goose, try typing -help after my name')
    return threshold


async def set_threshold(message, message_content, threshold):
    splits = message_content.split('-')
    cleaned_splits = []
    for split in splits:
        cleaned_splits.append(split.strip())
    new_threshold = cleaned_splits[2]
    if is_int(new_threshold) and 0 < int(new_threshold) <= 100:
        await message.channel.send('annoyance threshold was at '+str(threshold)+'\n setting new annoyance '
                                                                           'threshold to ' + new_threshold + '% chance')
        threshold = int(new_threshold) / 100
    else:
        await message.channel.send('not a valid threshold')
    return threshold

set_starter_threshold()
keep_alive()
client.run(os.getenv('TOKEN'))
