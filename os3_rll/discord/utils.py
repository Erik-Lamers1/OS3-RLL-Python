import discord
import re
import random
from logging import getLogger

from os3_rll.conf import settings

logger = getLogger(__name__)
discord_regex = re.compile("^.{2,32}#[0-9]{4}$")


def not_implemented():
    developer = get_player(random.choice(settings.DEVELOPERS))
    return "This command is not finished because {} is lazy as f*ck".format(developer.mention)


def pebkak():
    responses = [
        "I cannot believe what a stupid DUCK you really are...\n Please do kill -9 $(pgrep yourself)\n",
        "Is it that difficult to type, do you have butter fingers?\n",
        "OH MY GOD you are stupid, please rm -rf ./your_life\n",
        "WHAHAHAHAHAhahahaHAHAHAA, seriously you can't even operate a normal discord bot.\n",
    ]
    return random.choice(responses)


def create_embed(data, include_thumbnail=True):
    embed = discord.Embed(title=data["title"], description=data["description"], url=settings.WEBSITE, color=data["colour"])
    if include_thumbnail:
        embed.set_thumbnail(url=settings.DISCORD_EMBED_THUMBNAIL)
    embed.set_footer(text=data["footer"])
    return embed


def get_player(p):
    """ Get player by name/mention
        params:
            Can either be a string with the nickname
            or the mention: <@00000000000001>
            or the full discord name: NickName#0001

        returns: discord.Member or None
    """

    # Iterates over all the members the bot can see. (have to be members of guilds that it is connected too)
    # We import the bot here, because our design is stupid and can cause circular imports
    # TODO: Think of a more logical / better file structure
    # pylint: disable=import-outside-toplevel
    from os3_rll.discord.client import bot

    members = bot.get_all_members()
    player = None

    if p.startswith("<@!"):
        player_id = p[3:-1]
        logger.debug("got a mention for player_id {}".format(player_id))
        for member in members:
            logger.debug("check mentions if {} == {}".format(member.id, player_id))
            if str(member.id) == player_id:
                player = member
                break
    if discord_regex.match(p):
        logger.debug("got a discord user name and discriminator {}".format(p))
        for member in members:
            logger.debug("check if {0} == {1.name}#{1.discriminator}".format(p, member))
            if member.name == p.split("#")[0] and str(member.discriminator) == p.split("#")[1]:
                player = member
                break
    else:
        for member in members:
            logger.debug("check name if {} == {}".format(member.name, p))
            if member.name == p:
                player = member
                break
    # TODO: unhandled exception, return None if fail for now. This currently breaks the player model
    # if player is None:
    #     raise TypeError

    return player
