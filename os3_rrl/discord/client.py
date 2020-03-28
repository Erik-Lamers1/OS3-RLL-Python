import discord
from logging import getLogger

from os3_rrl.conf import settings


logger = getLogger(__name__)


def discord_client():
    logger.debug('Initializing Discord client')
    client = discord.Client()
    while True:
        client.run(settings.DISCORD_TOKEN)
