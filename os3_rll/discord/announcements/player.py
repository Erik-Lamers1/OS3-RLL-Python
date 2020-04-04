from logging import getLogger

from os3_rll.discord.utils import create_embed, get_player

logger = getLogger(__name__)


def announce_rankings(ranks : dict):
    """Generates an announcement for the current rankings.
       Params:
           ranks: Dictionary of rankings, with {'discord.Member':'rank'}
       return:
           Dictionary with content, title, description, footer and colour as keys.
    """
    sorted_ranks = {get_player(k): v for k, v in sorted(ranks.items(), key=lambda item: item[1])}
    champion = next(iter(sorted_ranks.keys()))
    description = ""

    for k, v in sorted_ranks.items():
        description += '{0:2}. {1}\n'.format(v, k.name + '#' + str(k.discriminator))

    try:
        embed = {'title': "**{} is the current champion.**".format(champion.name + "#" + str(champion.discriminator)),
                 'description': "{}".format(description),
                 'footer': "Become the best!",
                 'colour': 2234352}

        message = {'content': "Current OS3 Rocket League Ladder leaderboard:",
                   'embed': create_embed(embed)}

        # use this if you want to post the message via the bot's background routine
        # client.message_queue.put(message)
        # use this to return it with the players request.
        return message
    except TypeError:
        logger.error("Found NoneType Object for {}".format(ranks))



def announce_stats(stats : dict):
    """Generates an announcement for the current player statistics.
       Params:
           ranks: Dictionary of dictionary with stats
       return:
           Dictionary with content, title, description, footer and colour as keys.
    """
    description = ""
    first_stats = next(iter(stats.values()))
    table_heading = first_stats.keys()
    table_data = table_heading + list(zip([v.values() for k, v in stats.values()]))

    for i, d in enumerate(table_data):
        line = '|'.join(str(x).ljust(24) for x in d)
        description += '{}\n'.format(line)
        if i == 0:
            description += "{}\n".format('-' * len(line))



    #for player_id, player_stats in stats.items():
    #    description += '{}\n'.format('='*28)

    #    for stat_name, stat_value in player_stats.items():
    #        description += '{0:>24}: {1}\n'.format(stat_name, stat_value)


    try:
        embed = {'title': "** Player statistics **",
                 'description': "{}".format(description),
                 'footer': "Knowing better is doing better!",
                 'colour': 2234352}

        message = {'content': "Current OS3 Rocket League Ladder leaderboard:",
                   'embed': create_embed(embed)}

        # use this if you want to post the message via the bot's background routine
        # client.message_queue.put(message)
        # use this to return it with the players request.
        return message
    except TypeError:
        logger.error("Found NoneType Object for {}".format(stats))
