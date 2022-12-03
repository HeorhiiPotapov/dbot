""" main configuration file represents a sterter point of the application
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

handler = FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w',
)

intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)


def attachment_to_plot(file_name):
    PARAMS = {
        'filepath_or_buffer': file_name,
        'header': 0,
        'parse_dates': [0],
        'index_col': 0,
        # 'date_parser': lambda x: datetime.strptime('200'+x, '%Y-%m' )
    }
    series = read_csv(**PARAMS)
    series.index = series.index.to_period('M')
    model = ARIMA(series, order=(5, 1, 0))
    model_fit = model.fit()
    return model_fit.summary()


@client.event
async def on_ready() -> None:
    """Startup event handler
    """
    print(f'Our client have logged in as {client.user}')


@client.event
async def on_message(message: Message) -> Any:
    """New message received event handler
    """
    if message.author == client.user:
        return

    if message.attachments[0]:
        file_name: str = message.attachments[0].filename
        await message.attachments[0].save(file_name)
        await message.channel.send(attachment_to_plot(file_name))

    if message.content.startswith('$hi'):
        await message.channel.send("Hi there! What's up?")


def run() -> None:
    """startup MyClient
    """
    client.run(
        getenv('DISCORD_TOKEN'),
        log_handler=handler,
        log_level=DEBUG,
    )


if __name__ == '__main__':
    run()
