import discord
from logging import getLogger

from os3_rrl.conf import settings
from os3_rrl.actions import stub

logger = getLogger(__name__)

commands = {'get_ranking': stub.test_call_list,
            'get_active_challenges': stub.test_call_int,
            'create_challenge': stub.create_challenge,
            'complete_challenge': stub.complete_challenge,
            'reset_challenge': stub.reset_challenge
        }


async def on_message(message):
    logger.debug(f'saw a message: {message}')
    if message.channel.name == settings.DISCORD_CHANNEL:
        if message.content.startswith("$"):
           full_command = message.content[1:]
           cmd = full_command.split(' ')[0]
           params = full_command.split(' ')
           try:
               try:
                   res = commands[cmd](params)
               except ValueError:
                   logger.error(f'Found a PEBKAC, user provides stupid params: {params}')
                   res = stub.help()
           except KeyError:
               logger.error(f'Unknown command: {cmd}')


def discord_client():
    logger.debug('Initializing Discord client')

    client = discord.Client()

    logger.debug(f'{client.user is connected to the following guild:\n')
    logger.debug(f'{guild.name}(id: {guild.id})')

    while True:
        client.run(settings.DISCORD_TOKEN)
