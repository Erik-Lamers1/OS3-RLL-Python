import discord
import asyncio
import traceback
import sys
from discord.ext import commands
from logging import getLogger
from os import listdir
from os.path import isfile, join, basename
from discord.ext.commands import ExtensionAlreadyLoaded

from os3_rll.discord.queue import discord_message_queue as message_queue
from os3_rll.conf import settings
from os3_rll.discord import utils
from os3_rll.actions.challenge_tasks.check_uncompleted_challenges import check_uncompleted_challenges


logger = getLogger(__name__)
description = """A competition manager bot. This bot manages the Rocket Leage ladder."""

# This directory specifies what extensions (cogs which is a command aggregate) the bot should load at startup.
cogs_dir = settings.COGS_DIR
cogs_module_path = settings.COGS_RELATIVE_DIR.replace("/", ".")

bot = commands.Bot(command_prefix=commands.when_mentioned_or("$"), description=description, intents=utils.get_intents())


def is_rll_admin():
    """
    Command Checks decorator to check if a user has the RLL Admin role.
    """

    async def predicate(ctx):
        rlladmin = discord.utils.find(lambda role: role.name == "RLL Admin", ctx.guild.roles)
        return rlladmin in ctx.author.roles

    return commands.check(predicate)


@bot.command()
@is_rll_admin()
async def load(ctx, extension_name: str):
    """
    Loads an extension into the bot
    """
    try:
        bot.load_extension(extension_name)
        await ctx.send("{} loaded".format(extension_name))
    except (AttributeError, ImportError, ExtensionAlreadyLoaded) as e:
        logger.error("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        await ctx.send("Failed to load {} extension.".format(extension_name))


@bot.command()
@is_rll_admin()
async def unload(ctx, extension_name: str):
    """
    Unloads an extension from the bot.
    """
    bot.unload_extension(extension_name)
    await ctx.send("{} unloaded.".format(extension_name))


@bot.command()
@is_rll_admin()
async def listloaded(ctx):
    """
    Lists extensions currently loaded
    """
    await ctx.send(utils.not_implemented)


@bot.command()
@is_rll_admin()
async def listavailable(ctx):
    """
    Lists extensions available
    """
    await ctx.send(utils.not_implemented)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == settings.DISCORD_GUILD:
            logger.info("{} is connected to the following guild:".format(bot.user))
            logger.info("{}(id: {})".format(guild.name, guild.id))
            logger.debug("loading modules from module path - {}".format(cogs_module_path))
            logger.debug("loading modules from filesystem path - {}".format(cogs_dir))
            module_list = [basename(f).replace(".py", "") for f in listdir(cogs_dir) if isfile(join(cogs_dir, f)) and f != "__init__.py"]
            logger.info("start loading modules {}".format(", ".join(module_list)))
            for extension in module_list:
                try:
                    module = cogs_module_path + "." + extension
                    logger.debug("loading module: {}".format(module))
                    bot.load_extension(module)
                except commands.ExtensionError as e:
                    logger.error("{} - {}".format(type(e).__name__, e))
                    if not isinstance(e, commands.ExtensionAlreadyLoaded):
                        logger.error("Stack Trace", exc_info=True)
                except discord.DiscordException as e:
                    logger.error("Caught general discord Exception: {}, with message: {}".format(type(e).__name__, e))
                    logger.error("Stack Trace", exc_info=True)
            logger.info("completed loading modules")


@bot.event
async def on_command_error(ctx, error):
    logger.error("bot.on_command_error: {} - {}".format(type(error).__name__, error))
    traceback.print_exc()
    if error.__traceback__ is not None:
        logger.error("Stack Trace: {}".format(error), exc_info=True)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(utils.pebkak())
    elif isinstance(error, commands.CommandInvokeError):
        error_msg = str(error)
        if "Command raised an exception" in error_msg:
            await ctx.send(": ".join(error_msg.split(":")[1:]))
        else:
            await ctx.send("OUCH! that hurts. Better tell the devs to check the logs, something broke!")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Whooops, you are not allowed to do this. Ask an RLL Admin.")
    else:
        help_msg = "Try $help to find out how to use this command."
        msg = "{0.__name__}: {1}\n{2}\n".format(type(error), error, help_msg)
        await ctx.send(msg)


async def post():
    logger.debug("bot.post: started message posting background task")
    await bot.wait_until_ready()
    while not bot.is_closed():
        if not message_queue.empty():
            msg = message_queue.get()
            logger.debug("bot.post: got a message to post {}".format(msg))
            channel = discord.utils.get(bot.get_all_channels(), name=settings.DISCORD_CHANNEL)
            await channel.send(msg["content"], embed=msg["embed"])
        await asyncio.sleep(5)


async def check_expired_challenges():
    logger.debug("Checking for expired challenges")
    await bot.wait_until_ready()
    while not bot.is_closed():
        check_uncompleted_challenges()
        logger.debug("Done with checking for expired challenges, sleeping for {} seconds".format(settings.EXPIRED_CHALLENGES_WAIT_TIMER))
        await asyncio.sleep(settings.EXPIRED_CHALLENGES_WAIT_TIMER)


def discord_client():
    logger.info("Initializing Discord client")

    # We don't need Crons, we have background tasks
    for task in settings.DISCORD_BOT_BACKGROUND_TASKS:
        bot.loop.create_task(getattr(sys.modules[__name__], task)())

    try:
        while True:
            bot.run(settings.DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.warning("Caught KeyBoardInterrupt closing connection")
        bot.close()
    except RuntimeError:
        logger.info("Caught RunTimeError, this is probably the EventLoop closing, as we are shutting down. That's okay")
    finally:
        logger.info("Shutting down. Bye!")
        sys.exit(0)
