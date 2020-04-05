from logging import getLogger

from os3_rll.discord.utils import create_embed, get_player

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
                 'description': "This match should be played within one week or {} loses automatically.".format(
                     p2.mention),
                 'footer': "Good Luck!",
                 'colour': 2234352}

        message = {'content': "New Challenge!",
                   'embed': create_embed(embed)}

        # use this if you want to post the message via the bot's background routine
        # client.message_queue.put(message)
        # use this to return it with the players request.
        return message
    except TypeError:
        logger.error("Found NoneType Object for {} or {}".format(p1, p2))


def announce_winner(player1 : dict, player2 : dict):
    """Generates an announcement to be posted by the discord bot as an embed

       Params:
           p1: player1 dict with a discord.Member object and its score.
           p2: player2 dict with a discord.Member object and its score.

       return:
           Dictionary with content, title, description, footer and colour as keys.
    """
    title = ""
    if player1['score'] > player2['score']:
        title = "**{} has defeated {} with a score of {}-{}.**".format(str(player1['player']), str(player2['player']), player1['score'], player2['score'])
        description = "{} takes {}'s spot on the leaderboard!.".format(str(player1['player']), str(player2['player']))
        footer = "No dream is too big. ... "
        colour = "48393"
    else:
        title = "**{} successfully defended their spot against with a score of {}-{}".format(str(player2['player']), str(player1['player']), player2['score'], player1['score'])
        description = "That means that {} is now on a timeout of 1 week.".format(str(player1['player']))
        footer = "If you don't struggle, you'll never improve!"
        colour = "11540741"

    try:
        embed = {'title': title,
                 'description': description,
                 'footer': footer,
                 'colour': colour}

        message = {'content': "Challenge Completed!",
                   'embed': create_embed(embed)}

        # use this if you want to post the message via the bot's background routine
        # client.message_queue.put(message)
        # use this to return it with the players request.
        return message
    except TypeError:
        logger.error("Found {type(0)} {type(1)} Objects for {0} and {1}".format(player1, player2))

#def announce_reset(p1, p2):
#    """Generates an announcement for the current rankings.
#       Params:
#           ranks: List of rankings, with {'gamertag':'rank'}
#       return:
#           Dictionary with content, title, description, footer and colour as keys.
#    """
#    sorted_ranks = {k: v for k, v in sorted(
#    try:
#        embed = {'title': "**{} is the current champion**".format(),
#                 'description': "This match should be played within one week or {} loses automatically.".format(
#                     p2.mention),
#                 'footer': "Good Luck!",
#                 'colour': 2234352}
#
#        message = {'content': "New Challenge!",
#                   'embed': utils.create_embed(embed)}
#
#        # use this if you want to post the message via the bot's background routine
#        # client.message_queue.put(message)
#        # use this to return it with the players request.
#        return message
#    except TypeError:
#        logger.error("Found NoneType Object for {}".format(ranks))
