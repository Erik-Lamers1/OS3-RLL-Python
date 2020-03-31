import discord
import asyncio
import queue
import random
from discord.ext import commands, tasks
from logging import getLogger
from os3_rll.conf import settings
from os3_rll.actions import stub
from os3_rll.discord.annoucements.challenge import announce_challenge
from os3_rll.discord import utils

logger = getLogger(__name__)
message_queue = queue.Queue()
bot = commands.Bot(command_prefix='$')


def is_rll_admin():
    async def predicate(ctx):
        rlladmin = discord.utils.find(lambda role: role.name == 'RLL Admin', ctx.guild.roles)
        return rlladmin in ctx.author.roles

    return commands.check(predicate)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == settings.DISCORD_GUILD:
            break

    logger.info('bot.on_ready: {} is connected to the following guild:'.format(bot.user))
    logger.info('bot.on_ready: {}(id: {})'.format(guild.name, guild.id))


@bot.command()
async def hi(ctx, *args):
    """Say hi to the bot, maybe it'll greet you nicely."""
    logger.debug('bot.command.hi: called with {} arguments - {}'.format(len(args), ', '.join(args)))
    res = 'Hi {}\n'.format(ctx.author.mention)
    responses = ["How are you doing today? Wait that's retorical, I am a bot I do not care.\n",
                 "I was just looking at your rank. Did you know that you suck at rocket league? I heard some guy "
                 "SquishyMuffinz is best.\n",
                 "Please leave me alone. I am randomizing the rankings database to mess with Mr.Vin.\n",
                 "Due to COVID-19 I've had to reimplement the transport protocol from QUIC to plain UDP to avoid "
                 "handshakes.\n",
                 "Please do not bother me. I am looking into this Markov Chain theory. It should be able to give me "
                 "more human like responses.",
                 "What are you doing here? LOL, your rank is so low you should practice uninstall.\n"]
    res += random.choice(responses)
    await ctx.send(res)


@bot.command()
async def announce(ctx, p2: discord.Member):
    """Test call to announce a challenge."""
    logger.debug('bot.command.announce: called with {} - {}'.format(p2.name, p2))
    res = announce_challenge(ctx.author, p2)
    await ctx.send(res['content'], embed=res['embed'])


@bot.command()
async def get_ranking(ctx):
    """Returns the current top 5 ranking."""
    logger.debug('bot.command.get_ranking: called')
    res = stub.test_call_list("")
    await ctx.send(res)


@bot.command()
async def get_active_challenges(ctx):
    """Returns the number of active challenges."""
    logger.debug('bot.command.get_active_challenges: called')
    await ctx.send(stub.test_call_int(""))


@bot.command()
async def what(ctx, *args):
    """Allows you to ask a random question to the bot."""
    logger.debug('bot.command.what: called with {} arguments - {}'.format(len(args), ', '.join(args)))
    await ctx.send(stub.test_call_str(""))


@bot.command()
async def website(ctx):
    """Points you to the website of the Rocket-League-Ladder."""
    logger.debug('bot.command.website: called')
    await ctx.send('{} you can find the website at {}'.format(ctx.author.mention, settings.WEBSITE))


@bot.command()
async def get_challenge(ctx):
    """Gives your current challenge deadline."""
    logger.debug('bot.command.get_challenge: called')
    await ctx.send(utils.not_implemented())


@bot.command()
async def create_challenge(ctx, *args):
    """Creates a challenge between you and who you mention. """
    logger.debug('bot.command.create_challenge: called with {} arguments - {}'.format(len(args), ', '.join(args)))
    await ctx.send(utils.not_implemented())


@bot.command()
async def complete_challenge(ctx, *args):
    """Completes the challenge you are parcitipating in."""
    logger.debug('bot.command.complete_challenge: called with {} arguments - {}'.format(len(args), ', '.join(args)))
    await ctx.send(utils.not_implemented())


@bot.command()
async def reset_challenge(ctx, *args):
    """Resets the challenge you are parcitipating in."""
    logger.debug('bot.command.reset_challenge: called with {} arguments - {}'.format(len(args), ', '.join(args)))
    await ctx.send(utils.not_implemented())


@bot.command()
@is_rll_admin()
async def add_player(ctx, player: discord.Member):
    """Allows RRL Admins to add players to the Rocket-League-Ladder."""
    logger.debug('bot.command.add_player: called with {} - {}'.format(player.name, player))
    res = 'Yes master {}! Adding player {}'.format(ctx.author.mention, player.name)
    await ctx.send(res)


@bot.event
async def on_command_error(ctx, error):
    logger.error('bot.on_command_error: {} - {}'.format(type(error).__name__, error))
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(utils.pebkak())
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("OUCH! that hurts. Better tell the devs to check the logs, something broke!")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Whooops, you are not allowed to do this. Ask an RLL Admin.")
    else:
        await ctx.send(utils.bot_help())


async def post():
    logger.debug('bot.post: started message posting background task')
    await bot.wait_until_ready()
    while not bot.is_closed():
        if not message_queue.empty():
            msg = message_queue.get()
            logger.debug('bot.post: got a message to post {}'.format(msg))
            channel = discord.utils.get(bot.get_all_channels(), name=settings.DISCORD_CHANNEL)
            await channel.send(msg['content'], embed=msg['embed'])
        await asyncio.sleep(5)


def discord_client():
    logger.info('Initializing Discord client')
    bot.loop.create_task(post())

    while True:
        bot.run(settings.DISCORD_TOKEN)
