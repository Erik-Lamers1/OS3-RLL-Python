import discord
import random
from os3_rll.conf import settings
from os3_rll.discord import client
from logging import getLogger

logger = getLogger(__name__)

help_table = {'hi': 'Sends a rude greeting.',
            'announce': 'Sends a test announcement.',
            'get_ranking': 'Gives a list of the top 5 ranked player.',
            'get_active_challenges': 'Returns the number of active challenges.',
            'what': 'Allows the user to ask a random question',
            'website': 'Returns the website of the Rocket-League-Ladder.',
            'get_challenge': 'Returns the challenge the calling player is participating in.',
            'create_challenge': 'Creates a challenge.',
            'complete_challenge': 'Completes a challenge; requires the score of each round',
            'reset_challenge': 'Resets an active challenge.',
            'help': 'Either returns this or insults the user.'
            }


def not_implemented():
    developers = ['SyntheticOxygen', 'Mr. Vin', 'Mr. Vin', 'Mr. Vin', 'Mr. Vin', 'Pandabeer']
    developer = get_player(random.choice(developers))
    return 'This command is not finished because {} is lazy as f*ck'.format(developer.mention)


def bot_help():
    logger.debug('utils.bot_help: called')
    res = 'This bot supports the following commands:\n'
    for k,v in help_table.items():
        res += '\t ${}  -  {}'.format(k,v)
    pass


def pebkak():
    responses =['I cannot believe what a stupid FUCK you really are...\n Please do kill -9 $(pgrep yourself)\n',
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
        logger.debug("bot.get_player: got a mention for player_id {}".format(player_id))
        for member in members:
            logger.debug("bot.get_player: check mentions if {} == {}".format(member.id, player_id))
            if str(member.id) == player_id:
                player = member
                break
    else:
        for member in members:
            logger.debug("bot.get_player: check name if {} == {}".format(member.name, player))
            if member.name == p:
                player = member
                break

    if player is None:
        raise TypeError

    return player
