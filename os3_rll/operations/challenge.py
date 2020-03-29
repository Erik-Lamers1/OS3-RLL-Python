from logging import getLogger
from time import time

from os3_rll.mysql.db import Database
from os3_rll.actions.player import Player

logger = getLogger(__name__)


def get_challenge(args):
    """
    Return the outstanding challenge of the requesting player, if any.
    :type args: Player ID
    """
    db = Database()
    logger.debug('actions.challenge.Challenge.get_challenge: called with {}'.format(args))
    # Get the player ID
    pid = Player.get_id_by_gamertag(args[0].name)
    logger.debug('actions.challenge.Challenge.get_challenge: found player {} with id {}'.format(args[0].name, pid))
    db.execute('SELECT date, p1, p2 FROM challenges WHERE p1 = "{}" AND winner IS NULL'.format(pid))
    res = db.fetchone()
    logger.debug('actions.challenge.Challenge.get_challenge: got database result: {}'.format(res))
    if res is None:
        return "No outstanding challenges for player {} with pid {} found.".format(args[0].name, pid)
    else:
        return "A challenge is active until {} between {} and {}".format(res[0], res[1], res[2])


def update_player_rank(player, r):
    """
    Updates the rank of the player to the new rank r. All player ranks between the old and new rank are increased
    by 1.
    :param player: The Player object
    :param r: The new rank of the player
    """
    db = Database()
    # 'UPDATE users SET rank = rank + 1 WHERE rank >= {} AND rank < {}'.format(r, player.rank)
    db.execute('UPDATE users SET rank = rank + 1 WHERE rank >= {} AND rank < {}'.format(r, player.rank))
    # Update player.rank = r
    db.execute('UPDATE users SET rank={} WHERE id={}'.format(r, player.id))


def do_player_sanity_check(p1, p2):
    if p1.challenged:
        raise Exception('{} is already challenged'.format(p1))

    if p2.challenged:
        raise Exception('{} is already challenged'.format(p2))

    # Check if the rank of player 1 is lower than the rank of player 2:
    if p1.rank < p2.rank:
        raise Exception('The rank of {} is lower than of {}'.format(p1, p2))

    # Check if the ranks are the same; this should not happen
    if p1.rank == p2.rank:
        raise Exception("The ranks of both players are the same. This should not happen. EVERYBODY PANIC!!!")

    # Check if the timeout of player 1 has expired
    if p1.timeout > int(time()):
        raise Exception("The timeout counter of {} is still active".format(p1))


def create_challenge_entry(p1, p2):
    db = Database()
    db.execute('INSERT INTO challenges (date, p1, p2) VALUES (NOW(), {}, {})'.format(p1.id, p2.id))

