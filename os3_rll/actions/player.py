from logging import getLogger

from os3_rll.models.db import Database, DBException
from os3_rll.models.player import Player
from os3_rll.operations.player import get_all_player_ids_ordered, get_average_goals_per_challenge

logger = getLogger(__name__)


def get_player_ranking():
    """
    Gets the current player ranking from the DB

    returns dict: {str discord: int rank, ...}
    """
    players = {}
    logger.info('Getting current player ranking from DB')
    with Database() as db:
        db.execute('SELECT discord, rank FROM users WHERE rank > 0 ORDER BY rank')
        if db.rowcount == 0:
            raise DBException('No players found')
        rows = db.fetchall()
        for row in rows:
            # Fill the dict with discord => rank
            players[row[0]] = row[1]
    return players


def get_player_stats():
    """
    Get all the player stats
    returns dict of dicts: ->
        { player_id: {
            name                    -> str gamertag,
            discord                 -> str discord,
            rank                    -> int rank,
            wins                    -> int wins,
            losses                  -> int losses
            is_challenged
            avg_goals_per_challenge -> int goals
            },
            ...
        }
    """
    players = {}
    logger.info('Retrieving player stats')
    ids = get_all_player_ids_ordered()
    for player in ids:
        # Get the basic info
        with Player(player) as p:
            players[p.id] = {
                "name": p.gamertag,
                "discord": p.discord,
                "rank": p.rank,
                "wins": p.wins,
                "losses": p.losses,
                "is_challenged": p.challenged
            }
        # Now get the average goals per challenge
        players[player]["avg_goals_per_challenge"] = get_average_goals_per_challenge(player)
    return players
