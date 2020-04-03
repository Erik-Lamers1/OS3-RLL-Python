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
                 'description': "This match should be played within one week or {} loses automatically.".format(
                     p2.mention),
                 'footer': "Good Luck!",
                 'colour': 2234352}

        message = {'content': "New Challenge!",
                   'embed': utils.create_embed(embed)}

        # use this if you want to post the message via the bot's background routine
        # client.message_queue.put(message)
        # use this to return it with the players request.
        return message
    except TypeError:
        logger.error("Found NoneType Object for {} or {}".format(p1, p2))


def announce_rankings(ranks : dict):
    """Generates an announcement for the current rankings.
       Params:
           ranks: Dictionary of rankings, with {'discord.Member':'rank'}
       return:
           Dictionary with content, title, description, footer and colour as keys.
    """
    sorted_ranks = {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1])}
    champion = next(iter(sorted_ranks.keys()))
    description = ""

    for k, v in sorted_ranks.items():
        description += '{0:2}. {1}\n'.format(v, k.name + '#' + str(k.discriminator))

    try:
        embed = {'title': "**{} is the current champion.**".format(champion.name + "#" + str(champion.discriminator)),
                 'description': "{}".format(description),
                 'footer': "Become the best!",
                 'colour': 2234352}

        message = {'content': "Current OS3 Rocket League Ladder leaderboard",
                   'embed': utils.create_embed(embed)}

        # use this if you want to post the message via the bot's background routine
        # client.message_queue.put(message)
        # use this to return it with the players request.
        return message
    except TypeError:
        logger.error("Found NoneType Object for {}".format(ranks))



def announce_winner(winner, loser):
    """Generates an announcement to be posted by the discord bot as an embed

       Params:
           p1: player1 (the winner) as a discord.Member object.
           p2: player2 (the loser) as a discord.Member object.

       return:
           Dictionary with content, title, description, footer and colour as keys.
    """
    try:
        embed = {'title': "**{} has won a challenge {}.**".format(winner.name, loser.name),
                 'description': "Mr. Vin is an asshole.",
                 'footer': "Omg {} you are such a noob.".format(loser.name),
                 'colour': 2234352}

        message = {'content': "Challenge Completed!",
                   'embed': utils.create_embed(embed)}

        # use this if you want to post the message via the bot's background routine
        # client.message_queue.put(message)
        # use this to return it with the players request.
        return message
    except TypeError:
        logger.error("Found NoneType Object for {} or {}".format(winner, loser))

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
