from logging import getLogger
from datetime import datetime

from os3_rll.models.db import Database
from os3_rll.models.challenge import ChallengeException
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


def do_challenge_sanity_check(p1, p2):
    """
    Preform checks for a new challenge to be created

    param os3_rll.models.player.Player() p1: The player model for player 1
    param os3_rll.models.player.Player() p2: The player model for player 2
    raises ChallengeException on sanity check failure
    """
    if p1.challenged:
        raise ChallengeException('{} is already challenged'.format(p1.gamertag))

    if p2.challenged:
        raise ChallengeException('{} is already challenged'.format(p2.gamertag))

    # Check if the rank of player 1 is lower than the rank of player 2:
    if p1.rank < p2.rank:
        raise ChallengeException('The rank of {} is lower than of {}'.format(p1.gamertag, p2.gamertag))

    # Check if the ranks are the same; this should not happen
    if p1.rank == p2.rank:
        raise ChallengeException(
            "The ranks of both player {} and player {} are the same. This should not happen. EVERYBODY PANIC!!!".format(
                p1.gamertag, p2.gamertag
            )
        )

    # Check if the timeout of player 1 has expired
    if p1.timeout > datetime.now():
        raise ChallengeException("The timeout counter of {} is still active".format(p1.gamertag))


def create_challenge_entry(p1, p2):
    db = Database()
    db.execute('INSERT INTO challenges (date, p1, p2) VALUES (NOW(), {}, {})'.format(p1.id, p2.id))

