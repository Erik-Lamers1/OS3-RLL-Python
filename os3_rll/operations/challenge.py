from logging import getLogger
from datetime import datetime

from os3_rll.models.challenge import ChallengeException
from os3_rll.models.player import Player
from os3_rll.models.db import Database

logger = getLogger(__name__)


def do_challenge_sanity_check(p1, p2, may_already_by_challenged=False):
    """
    Preform checks for a new challenge to be created

    param os3_rll.models.player.Player() p1: The player model for player 1
    param os3_rll.models.player.Player() p2: The player model for player 2
    param bool may_already_by_challenged: If True skips the player.challenged check
    raises ChallengeException on sanity check failure
    """
    if p1.challenged and not may_already_by_challenged:
        raise ChallengeException('{} is already challenged'.format(p1.gamertag))

    if p2.challenged and not may_already_by_challenged:
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


def process_completed_challenge_args(args):
    """
    Processes the completed challenge arguments
    args str: of the played matches sperated by spaces and scores by dashes.
        Example "1-2 5-3 2-4" corresponds to 3 matches played with the first match ending in 1-2, the second in 5-3 ect.
    """
    p1_wins, p2_wins, p1_score, p2_score = 0, 0, 0, 0
    matches = args.split()
    for match in matches:
        scores = match.split('-')
        if len(scores) != 2:
            raise ChallengeException('Unable to parse challenge arguments')
        # Assign the win to the player with the highest score
        scores[0] = int(scores[0])
        scores[1] = int(scores[1])
        if scores[0] > scores[1]:
            p1_wins += 1
        elif scores[1] > scores[0]:
            p2_wins += 1
        # Assign the amount of goals
        p1_score += scores[0]
        p2_score += scores[1]
    # Check for a draw
    if p1_wins == p2_wins:
        raise ChallengeException('Draws are not allowed')
    return p1_wins, p2_wins, p1_score, p2_score


def get_player_objects_from_complete_challenge_info(message_author):
    """
    Search for a challenge in the DB corresponding to the message_author

    param str message_author: The discord_user that send the message (eg. Pandabeer#2202)
    """
    with Database() as db:
        db.execute_prepared_statement('SELECT id FROM users WHERE discord=%s', (message_author,))
        if db.rowcount != 1:
            raise ChallengeException('Player with discord username {}, not found'.format(message_author))
        user_id = db.fetchone()[0]
        db.execute_prepared_statement(
            'SELECT p1, p2 FROM challenges WHERE (p1=%s OR p2=%s) AND winner IS NULL ORDER BY id DESC',
            (user_id, user_id)
        )
        if db.rowcount == 0:
            raise ChallengeException('No challenges found')
        p1, p2 = db.fetchone()
    return Player(p1), Player(p2)
