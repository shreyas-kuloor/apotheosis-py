import logging
import discord
import os

logger = logging.FileHandler(filename='apotheosis.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logging.info('{} is connected.'.format(client.user.name))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run(os.environ.get('DISCORD_BOT_TOKEN'), log_handler=logger)
