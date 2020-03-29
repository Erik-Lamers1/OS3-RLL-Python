from asyncio import get_running_loop
from logging import getLogger

from os3_rll.discord import client

logger = getLogger(__name__)


def announce_challenge(players):
    """Generates an announcement to be posted by the discord bot as an embed

       Params:
           players: (list of players)
           p1: player1 (the challenger) its discord name.
           p2: player2 (the challengee) its discord name.

       return:
           Dictionary with content, title, description, footer and colour as keys.
    """
    # Get the mentions of the players. Raises a TypeError if it cannot find the players
    try:
        loop = get_running_loop()
        author = players[0]
        p1 = players[0].name
        p2 = players[1][0]
        challenger, challengee = client.get_player_mentions(p1, p2)
        message = {'content': "New Challenge!",
                   'title': "**{} challenges {}.**".format(challenger, challengee),
                   'description': "This match should be played within one week or {} wins automatically.".format(
                       challenger),
                   'footer': "Good Luck!",
                   'colour': "2234352"}

        loop.create_task(client.post_embed(message))
    except TypeError:
        logger.error("actions.challenge.announce_challenge: Found NoneType Object for {} or {}".format(p1, p2))

    return "Ok..."
