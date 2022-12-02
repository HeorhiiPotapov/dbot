""" main configuration file represents a sterter point of the application
"""

import os
import dotenv
import discord
import logging


dotenv.load_dotenv('.env')

handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w',
)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    """Startup event handler
    """
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    """New message received event handler
    """
    if message.author == client.user:
        return

    if message.content.startswith('$hi'):
        await message.channel.send("Hi there! What's up?")


def run() -> None:
    """startup MyClient
    """
    client.run(
        os.getenv('DISCORD_TOKEN'),
        log_handler=handler,
        log_level=logging.DEBUG,
    )


if __name__ == '__main__':
    run()
