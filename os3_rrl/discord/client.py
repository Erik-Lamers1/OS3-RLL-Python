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

client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == settings.DISCORD_GUILD:
            break

    logger.debug(f'{client.user is connected to the following guild:\n')
    logger.debug(f'{guild.name}(id: {guild.id})')


@client.event
async def on_message(message):
    logger.debug(f'saw a message: {message}')
    channel = message.channel
    res = "Ok..."
    if channel.name == settings.DISCORD_CHANNEL:
        if message.content.startswith("$"):
           full_command = message.content.lower()[1:]
           cmd = full_command.split(' ')[0]
           params = full_command.split(' ')[1:]
           try:
               try:
                   res = commands[cmd](params)
               except ValueError:
                   logger.error(f'Found a PEBKAC, user provides stupid params: {params}')
                   res = stub.help()
           except KeyError:
               logger.error(f'Unknown command: {cmd}')

           await channel.send(res)


def discord_client():
    logger.debug('Initializing Discord client')

    while True:
        client.run(settings.DISCORD_TOKEN)
