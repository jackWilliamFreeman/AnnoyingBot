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


@client.event
async def on_message(message):
    annoyance_threshold = random.uniform(0, 1)
    threshold = .1
    if message.author == client.user:
        return

    if message.content.startswith('$annoyingbot'):
        message_content = message.content

        if message_content.lower() == '$annoyingbot -help':
            await message.channel.send('Options:\n'
                                       '-hello annoyingBot will say hello\n'
                                       '-help gives you options\n'
                                       '-threshold -int sets threshold for activation based on int ie. 50 = 50%')

        if message_content.lower() == '$annoyingbot -hello':
            await message.channel.send('sup carnt?')

        if message_content.lower().startswith('$annoyingbot -threshold'):
            splits = message_content.split('-')
            cleaned_splits = []
            for split in splits:
                cleaned_splits.append(split.strip())
            new_threshold = cleaned_splits[2]
            if is_int(new_threshold) and 0 < int(new_threshold) <= 100:
                await message.channel.send('setting new annoyance threshold to ' + new_threshold + '% chance')
                threshold = int(new_threshold) / 100
            else:
                await message.channel.send('not a valid threshold')

        if message_content.lower() == '$annoyingbot':
            await message.channel.send('give me some real instructions you goose, try typing -help after my name')

    if message.author.id == 368751796945944577 and annoyance_threshold <= threshold:
        print('annoying target')
        await message.channel.send('Ian you smell')


keep_alive()
client.run(os.getenv('TOKEN'))
