import discord
import asyncio
import queue
from discord.ext import commands, tasks
from logging import getLogger

from os3_rll.conf import settings
from os3_rll.actions import stub
from os3_rll.discord.annoucements.challenge import announce_challenge
from os3_rll.operations.challenge import get_challenge

logger = getLogger(__name__)

commands = {'hi': stub.hello,
            'announce': announce_challenge,
            'get_ranking': stub.test_call_list,
            'get_active_challenges': stub.test_call_int,
            'what': stub.test_call_str,
            'website': stub.get_website,
            'get_challenge': get_challenge,
            'create_challenge': stub.create_challenge,
            'complete_challenge': stub.complete_challenge,
            'reset_challenge': stub.reset_challenge,
            'help': stub.stub_help
            }

bot = discord.Client()
message_queue = queue.Queue()


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == settings.DISCORD_GUILD:
            break

    logger.info('{} is connected to the following guild:\n'.format(bot.user))
    logger.info('{}(id: {})'.format(guild.name, guild.id))


@bot.event
async def on_message(message):
    logger.info('saw a message: {}'.format(message))  #
    channel = message.channel
    res = "Ok..."
    if channel.name == settings.DISCORD_CHANNEL:
        if message.content.startswith("$"):
            logger.info('message.content: {}'.format(message.content))
            logger.info('message.author: {}#{}'.format(message.author.name, message.author.discriminator))
            full_command = message.content[1:]
            cmd = full_command.split(' ')[0]
            params = [message.author, full_command.split(' ')[1:]]
            try:
                try:
                    res = commands[cmd](params)
                except (TypeError, ValueError) as e:
                    logger.error('Found a PEBKAC, user provides stupid params: {}\n'.format(params) +
                                 'This resulted in the following error:\n{}\n'.format(str(e))
                                )
                    res = commands['help'](params)
            except KeyError:
                logger.error('Unknown command: {}'.format(cmd))

            await channel.send(res)


async def post_embed():
    logger.debug('client.post_embed: started post_embed background task')
    await bot.wait_until_ready()
    logger.debug('client.post_embed: bot is ready')

    channel = discord.utils.get(bot.get_all_channels(), name=settings.DISCORD_CHANNEL)

    while not bot.is_closed():
        if not message_queue.empty():
            msg = message_queue.get()
            logger.debug('client.post_embed: got an embed to post {}'.format(msg))
            embed = discord.Embed(title=msg['title'],
                                  description=msg['description'],
                                  url=settings.WEBSITE,
                                  color=msg['colour'])

            embed.set_thumbnail(url=settings.DISCORD_EMBED_THUMBNAIL)
            embed.set_footer(text=msg['footer'])

            await channel.send(msg['content'], embed=embed)
        logger.debug('client.post_embed: running_loop')
        await asyncio.sleep(5)


def get_player_mentions(p1, p2):
    # Iterates over all the members the bot can see. (have to be members of guilds that it is connected too)
    members = bot.get_all_members()
    challenger = None
    challengee = None
    for member in members:
        logger.debug("discord.client.get_player_mentions: looking at member {}".format(member.name))
        if member.name == p1:
            challenger = member.mention
        if member.name == p2:
            challengee = member.mention

    if challenger is None or challengee is None:
        raise TypeError

    return challenger, challengee


def discord_client():
    logger.info('Initializing Discord client')

    bot.loop.create_task(post_embed())

    while True:
        bot.run(settings.DISCORD_TOKEN)
