""" main configuration file represents a sterter point of the application
"""

import os
import dotenv
import discord
import logging

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

dotenv.load_dotenv('.env')

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
APP_ID = os.getenv('APP_ID')
PUBLIC_KEY = os.getenv('PUBLIC_KEY')
GUILD_ID = os.getenv('GUILD_ID')


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """ended up all preps"""
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    """new message received"""
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


def run() -> None:
    """startup MyClient"""
    client.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)


if __name__ == '__main__':
    run()
