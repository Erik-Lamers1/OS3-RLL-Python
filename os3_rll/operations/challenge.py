from logging import getLogger
from datetime import datetime

from os3_rll.models.challenge import ChallengeException

logger = getLogger(__name__)


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
