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


intents = discord.Intents.all()
client = discord.Client(intents=intents)
guild_name = 'MWM'
members = ''
global insultee
insultee = 'ianforcements'
global insultee_id
insultee_id = 368751796945944577

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await get_members()


async def get_members():
    for guild in client.guilds:
        if guild.name == guild_name:
            break
    global members
    members = guild.members

def set_starter_threshold():
    global globalFactor
    globalFactor = .1


@client.event
async def on_message(message):
    annoyance_threshold = random.uniform(0, 1)
    insults = [insultee + ' you have bad hair', insultee + ' you smell', insultee + ' your sense of fashion is bad',
               insultee + ' is not masculine']

    if message.author == client.user:
        return

    if message.content.startswith('$annoyingbot'):
        global globalFactor
        globalFactor = await handle_annoyingbot_commands(message, globalFactor)

    insult = random.choice(insults)
    if message.author.id == insultee_id and annoyance_threshold <= globalFactor:
        print('annoying target')
        await message.channel.send(insult)

    if message.author.id == 752655419486371982:
        print('Encouraging Drinking')
        await message.channel.send('Ignore Drunkbot, drunk you is a better you')


async def handle_annoyingbot_commands(message, threshold):
    message_content = message.content
    if message_content.lower() == '$annoyingbot -help':
        await message.channel.send('Options:\n'
                                   '-hello annoyingBot will say hello\n'
                                   '-help gives you options\n'
                                   '-retarget -string retarget the annoying bot at others\n'
                                   '-threshold -int sets threshold for activation based on int ie. 50 = 50%')
    if message_content.lower() == '$annoyingbot -hello':
        await message.channel.send('sup carnt?')
    if message_content.lower().startswith('$annoyingbot -threshold'):
        threshold = await set_threshold(message, message_content, threshold)
    if message_content.lower().startswith('$annoyingbot -retarget'):
        await get_members()
        cleaned_splits = await get_cleaned_splits(message_content)
        target = cleaned_splits[2]
        found_member = False
        for member in members:
            if member.display_name.lower() == target.lower():
                global insultee
                global insultee_id
                await message.channel.send('old target = '+insultee+' new target = '+member.display_name)
                insultee = member.display_name
                insultee_id = member.id
                found_member = True
        if(found_member == False):
            await message.channel.send('Could not find member named '+target)

    if message_content.lower() == '$annoyingbot':
        await message.channel.send('give me some real instructions you goose, try typing -help after my name')
    return threshold


async def set_threshold(message, message_content, threshold):
    cleaned_splits = await get_cleaned_splits(message_content)
    new_threshold = cleaned_splits[2]
    if is_int(new_threshold) and 0 < int(new_threshold) <= 100:
        await message.channel.send('annoyance threshold was at ' + str(threshold) + '\n setting new annoyance '
                                                                                    'threshold to ' + new_threshold + '% chance')
        threshold = int(new_threshold) / 100
    else:
        await message.channel.send('not a valid threshold')
    return threshold


async def get_cleaned_splits(message_content):
    splits = message_content.split('-')
    cleaned_splits = []
    for split in splits:
        cleaned_splits.append(split.strip())
    return cleaned_splits

set_starter_threshold()
keep_alive()
client.run('')
