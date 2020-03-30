from logging import getLogger

from os3_rll.discord import utils

logger = getLogger(__name__)


def announce_challenge(p1, p2):
    """Generates an announcement to be posted by the discord bot as an embed

       Params:
           p1: player1 (the challenger) as a discord.Member object.
           p2: player2 (the challengee) as a discord.Member object.

       return:
           Dictionary with content, title, description, footer and colour as keys.
    """
    try:
        embed = {'title': "**{} challenges {}.**".format(p1.name, p2.name),
                 'description': "This match should be played within one week or {} loses automatically.".format(p2.mention),
                 'footer': "Good Luck!",
                 'colour': 2234352}

        message = {'content': "New Challenge!",
                   'embed': utils.create_embed(embed)}

        #use this if you want to post the message via the bot's background routine
        #client.message_queue.put(message)
        #use this to return it with the players request.
        return message
    except TypeError:
        logger.error("actions.challenge.announce_challenge: Found NoneType Object for {} or {}".format(p1, p2))
