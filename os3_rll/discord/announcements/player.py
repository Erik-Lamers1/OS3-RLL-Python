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
    sorted_ranks = {get_player(k): v for k, v in sorted(ranks.items(), key=lambda item: item[1][0])}
    champion = next(iter(sorted_ranks.valuess()))[1]
    description = ""

    for k, v in sorted_ranks.items():
        if get_player(k.name + '#' + str(k.discriminator)) is None:
            raise PlayerException('Player returned from database does not have a valid Discord account')

        description += '{0:2}. {1}\n'.format(v[0], v[1])

    try:
        embed = {'title': "**{} is the current champion.**".format(champion),
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
    longest_key = 0
    longest_value = 0

    for player_id, player_stats in stats.items():
        for k, v in player_stats.items():
            if len(k) > longest_key:
                longest_key = len(k)
            if len(str(v)) > longest_value:
                longest_value = len(str(v))

    padding = longest_key + longest_value + 3
    for player_id, player_stats in stats.items():
        description += '{}\n'.format('='*padding)

        for stat_name, stat_value in player_stats.items():
            description += '{0:>24}: {1}\n'.format(stat_name, stat_value)

    try:
        embed = {'title': "** Player statistics **",
                 'description': "```{}```".format(description),
                 'footer': "Knowing better is doing better!",
                 'colour': 2234352}

        message = {'content': "Current OS3 Rocket League Ladder Player Statistics:",
                   'embed': create_embed(embed)}

        # use this if you want to post the message via the bot's background routine
        # client.message_queue.put(message)
        # use this to return it with the players request.
        return message
    except TypeError:
        logger.error("Found NoneType Object for {}".format(stats))


def create_stats_table(stats: dict):
    table = ""
    first_stats = next(iter(stats.values()))
    table_heading = list(first_stats.keys())
    table_data = [list(v.values()) for v in stats.values()]
    table += '|'
    for e in table_heading:
        if e == "avg_goals_per_challenge":
            e = "goal avg."
        line = ''.join("  {}|".format(str(e).ljust(21)))
        table += '{}'.format(line)
    table += '\n{}\n'.format('-' * len(table))
    for player_entry in table_data:
        table += '|'
        for stat in player_entry:
            line = ''.join("  {}|".format(str(stat).ljust(21)))
            table += '{}'.format(line)
        table += '\n'

    return table
