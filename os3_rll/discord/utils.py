import discord
import re
import random
from os3_rll.conf import settings
from os3_rll.discord import client
from logging import getLogger

logger = getLogger(__name__)
discord_regex = re.compile('^.{2,32}#[0-9]{4}$')

def not_implemented():
    developers = ['SyntheticOxygen', 'Mr. Vin', 'Mr. Vin', 'Mr. Vin', 'Mr. Vin', 'Pandabeer']
    developer = get_player(random.choice(developers))
    return 'This command is not finished because {} is lazy as f*ck'.format(developer.mention)


def pebkak():
    responses = ['I cannot believe what a stupid FUCK you really are...\n Please do kill -9 $(pgrep yourself)\n',
                 'Is it that difficult to type, do you have butter fingers?\n',
                 'OH MY GOD you are stupid, please rm -rf ./your_life\n',
                 "WHAHAHAHAHAhahahaHAHAHAA, seriously you can't even operate a normal discord bot.\n"]
    return random.choice(responses)


def create_embed(data):
    embed = discord.Embed(title=data['title'],
                          description=data['description'],
                          url=settings.WEBSITE,
                          color=data['colour'])
    embed.set_thumbnail(url=settings.DISCORD_EMBED_THUMBNAIL)
    embed.set_footer(text=data['footer'])
    return embed


def get_player(p):
    # Iterates over all the members the bot can see. (have to be members of guilds that it is connected too)
    members = client.bot.get_all_members()
    player = None

    if p.startswith('<@!'):
        player_id = p[3:-1]
        logger.debug("got a mention for player_id {}".format(player_id))
        for member in members:
            logger.debug("check mentions if {} == {}".format(member.id, player_id))
            if str(member.id) == player_id:
                player = member
                break
    if discord_regex.match(p):
        logger.debug("got a discord user name and discriminator {}".format())
        for member in members:
            logger.debug("check if {} == {0.name}#{0.discriminator}".format(p, member))
            if member.name == p.split('#')[0] and str(member.discriminator) == p.split('#')[1]:
                player = member
                break
    else:
        for member in members:
            logger.debug("check name if {} == {}".format(member.name, p))
            if member.name == p:
                player = member
                break

    if player is None:
        raise TypeError

    return player
