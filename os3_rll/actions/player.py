from logging import getLogger

from os3_rll.models.db import Database, DBException
from os3_rll.models.player import Player
from os3_rll.operations.player import get_all_player_ids_ordered, get_average_goals_per_challenge
from os3_rll.utils.password import generate_password

logger = getLogger(__name__)


def get_player_ranking():
    """
    Gets the current player ranking from the DB

    returns dict: {str discord: int rank, ...}
    """
    players = {}
    logger.info("Getting current player ranking from DB")
    with Database() as db:
        db.execute("SELECT discord, rank, gamertag FROM users WHERE rank > 0 ORDER BY rank")
        if db.rowcount == 0:
            raise DBException("No players found")
        rows = db.fetchall()
        for row in rows:
            # Fill the dict with discord => rank
            players[row[0]] = (row[1], row[2])
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
            avg_goals_per_challenge -> float goals
            },
            ...
        }
    """
    players = {}
    logger.info("Retrieving player stats")
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
                "is_challenged": p.challenged,
            }
        # Now get the average goals per challenge
        players[player]["avg_goals_per_challenge"] = get_average_goals_per_challenge(player)
    return players


def add_player(name, gamertag, discord):
    """
    Creates a new player in the database.
    Params:
        str name -> the natural name of the player (e.g. klootviool)
        str gamertag -> the gamertag of the player (e.g. Klootviool NL)
        str discord -> the discord of the player (e.g. klootviool#1337)

    returns 2-tuple: (p: os3_rll.models.Player, password: str)
    """
    logger.debug("Adding player with properties: {}, {}, {}".format(name, gamertag, discord))
    password = generate_password()
    p = Player()
    p.name = name
    p.gamertag = gamertag
    p.discord = discord
    p.password = password
    p.save()
    return Player(Player.get_player_id_by_username(gamertag)), password


def reset_player_password(player, discord_name=False):
    """
    Resets the password for a player
    Params:
       str player: The gamertag or discord name of the player to reset the password for
       bool discord_name: Search for discord_name rather then gamertag if True

    return str: new password
    """
    logger.info("Resetting password for {}".format(player))
    p = Player(Player.get_player_id_by_username(player, discord_name=discord_name))
    password = generate_password()
    p.password = password
    p.save()
    return password
