import discord
from logging import getLogger

from os3_rll.conf import settings
from os3_rll.actions import stub
from os3_rll.actions import challenge

logger = getLogger(__name__)

commands = {'hi': stub.hello,
            'announce': challenge.Challenge.announce_challenge,
            'get_ranking': stub.test_call_list,
            'get_active_challenges': stub.test_call_int,
            'what': stub.test_call_str,
            'website': stub.get_website,
            'get_challenge': challenge.Challenge.get_challenge,
            'create_challenge': stub.create_challenge,
            'complete_challenge': stub.complete_challenge,
            'reset_challenge': stub.reset_challenge,
            'help': stub.stub_help
            }

client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == settings.DISCORD_GUILD:
            break

    logger.info('{} is connected to the following guild:\n'.format(client.user))
    logger.info('{}(id: {})'.format(guild.name, guild.id))


@client.event
async def on_message(message):
    logger.info('saw a message: {}'.format(message))  #
    channel = message.channel
    res = "Ok..."
    if channel.name == settings.DISCORD_CHANNEL:
        if message.content.startswith("$"):
            logger.info('message.content: {}'.format(message.content))
            logger.info('message.author: {}{}'.format(message.author.name, message.author.discriminator))
            full_command = message.content.lower()[1:]
            cmd = full_command.split(' ')[0]
            params = [message.author, full_command.split(' ')[1:]]
            try:
                try:
                    res = commands[cmd](params)
                except (TypeError, ValueError):
                    logger.error('Found a PEBKAC, user provides stupid params: {}'.format(params))
                    res = commands['help'](params)
            except KeyError:
                logger.error('Unknown command: {}'.format(cmd))

            await channel.send(res)


async def post_embed(msg):
    logger.info('client.post_embed: got an embed to post {}'.format(msg))
    channel = settings.DISCORD_CHANNEL
    embed = discord.Embed(title=msg['title'],
                          description=msg['description'],
                          url=settings.WEBSITE,
                          color=msg['colour'])

    embed.set_thumbnail("{}".format(settings.DISCORD_EMBED_THUMBNAIL))
    embed.set_footer(msg['footer'])

    await channel.send(content=msg['content'], embed=embedded_msg)


def get_player_mentions(p1, p2):
    # Iterates over all the members the bot can see. (have to be members of guilds that it is connected too)
    members = client.get_all_members()
    challenger = None
    challengee = None
    for member in members:
        if p1 == member.name:
            challenger = member.mention
        if p2 == member.name:
            challengee = member.mention

    if challenger is None or challengee is None:
        raise TypeError

    return (challenger, challengee)


def discord_client():
    logger.info('Initializing Discord client')

    while True:
        client.run(settings.DISCORD_TOKEN)
