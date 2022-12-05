""" The main project's file, used to startup application

    #! Configue watcher to have hot-reloading functionality:

    #? example placed bellow can be added to the client's on_ready event handler:
        from cogwatch import Watcher

        async def on_ready():
            watcher = Watcher(client, path='.', preload=True)
            await watcher.start()

    #? Also there's a way to use @watch decorator:
        from cogwatch import watch
        from discord.ext import commands

        class ExampleBot(commands.Bot):
            def __init__(self):
                super().__init__(command_prefix='!')

            @watch(path='commands')
            async def on_ready():
                print('Bot started success...')
"""

from typing import Any
from os import getenv
from dotenv import load_dotenv
from discord import Client, Intents, Message
from logging import FileHandler, DEBUG
from pandas import read_csv, DataFrame
from matplotlib import pyplot, pylab
from pandas.plotting import autocorrelation_plot
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA

load_dotenv()

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)


def read_attachment(file_name):
    PARAMS = {
        'filepath_or_buffer': file_name,
        'header': 0,
        'parse_dates': [0],
        'index_col': 0,
        # 'date_parser': lambda x: datetime.strptime('200'+x, '%Y-%m' )
    }
    return read_csv(**PARAMS)


def attachment_summary(file_name):
    series = read_attachment(file_name)
    series.index = series.index.to_period('M')
    model = ARIMA(series, order=(5, 1, 0))
    model_fit = model.fit()
    return model_fit.summary()


def plot_dataframe(df, title="", dpi=100):
    pyplot.figure(figsize=(15,4), dpi=dpi)
    pyplot.plot(df, color='tab:red')
    pyplot.gca().set(title=title)
    # pyplot.show()
    pyplot.imsave(fname=title+'.png')
    import os
    return title+'.png'


@client.event
async def on_ready() -> None:
    """Startup event handler
    """
    print(f"Our client have logged in as {client.user}")


@client.event
async def on_message(message: Message) -> Any:
    """New message received event handler
    """
    if message.author == client.user:
        return

    if message.attachments[0]:
        file_name: str = message.attachments[0].filename

        await message.attachments[0].save(
            fp=file_name,
            use_cached=True
        )

        await message.channel.send(
            plot_dataframe(
                df=read_attachment(file_name),
                title=file_name,
            )
        )
        await message.channel.send(
            attachment_summary(file_name)
        )

    if message.content.startswith('$hi'):
        await message.channel.send("Hi there! What's up?")


def run() -> None:
    """startup MyClient
    """
    handler = FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    client.run(getenv('DISCORD_TOKEN'), log_handler=handler, log_level=DEBUG)


if __name__ == '__main__':
    run()
