from logging import getLogger
from datetime import datetime

from os3_rll.models.challenge import Challenge, ChallengeException
from os3_rll.models.player import Player, PlayerException
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
        raise ChallengeException("{} is already challenged".format(p1.gamertag))

    if p2.challenged and not may_already_by_challenged:
        raise ChallengeException("{} is already challenged".format(p2.gamertag))

    # Check if the rank of player 1 is lower than the rank of player 2:
    if p1.rank < p2.rank:
        raise ChallengeException("The rank of {} is lower than of {}".format(p1.gamertag, p2.gamertag))

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
    logger.debug("Trying to parse challenge result, got the following user input {}".format(args))
    matches = args.split()
    for match in matches:
        scores = list(filter(None, match.split("-")))
        if len(scores) != 2:
            raise ChallengeException("Unable to parse challenge arguments")
        # Check for dummies who didn't pass the last score
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
        raise ChallengeException("Draws are not allowed")
    return p1_wins, p2_wins, p1_score, p2_score


def get_player_objects_from_challenge_info(player, should_be_completed=False, search_by_discord_name=True):
    """
    Search for a challenge in the DB corresponding to the player

    param bool should_be_completed: If the challenge should already be completed or not
    param bool search_by_discord_name: Searches for player by full discord_name instead of gamertag
    param str message_author: The discord_user that send the message (eg. Pandabeer#2202)
    returns tuple os3_rll.models.player.Player: (p1, p2)
    """
    if isinstance(player, str):
        player = Player.get_player_id_by_username(player, discord_name=search_by_discord_name)
    with Database() as db:
        db.execute_prepared_statement(
            "SELECT p1, p2 FROM challenges WHERE (p1=%s OR p2=%s) AND winner IS {} NULL ORDER BY id DESC".format(
                "NOT" if should_be_completed else ""
            ),
            (player, player),
        )
        if db.rowcount == 0:
            raise ChallengeException("No challenges found")
        p1, p2 = db.fetchone()
    return Player(p1), Player(p2)


def get_latest_challenge_from_player_id(player, should_be_completed=False):
    """
    Tries to find the latest challenge belonging to a player

    param int player: The player ID to search the challenges for
    param bool should_be_completed: If the challenge should already be completed or not
    returns os3_rll.models.challenge: if a challenge is found
    raises ChallengeException/PlayerException: on not found / on error
    """
    logger.info("Trying to get latest challenge from player with id {}".format(player))
    with Player(player) as p:
        if not p.challenged and not should_be_completed:
            raise PlayerException("Player {} is currently not in an active challenge".format(p.gamertag))
        # Try to find a challenge
        p.db.execute(
            "SELECT id FROM challenges WHERE (p1={0} OR p2={0}) AND winner is {1} NULL ORDER BY id LIMIT 1".format(
                p.id, "NOT" if should_be_completed else ""
            )
        )
        p.check_row_count()
        challenge = p.db.fetchone()[0]
    # Return the Challenge model
    return Challenge(challenge)
