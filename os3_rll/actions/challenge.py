from logging import getLogger
from datetime import datetime, timedelta
from copy import deepcopy

from os3_rll.models.player import Player
from os3_rll.models.challenge import Challenge, ChallengeException
from os3_rll.operations.challenge import do_challenge_sanity_check, process_completed_challenge_args
from os3_rll.operations.utils import check_date_is_older_than_x_days

logger = getLogger(__name__)


def create_challenge(p1, p2, search_by_discord_name=True):
    """
    Create a challenge between p1 and p2. Where p1 is the one challenging and p2 is the one defending

    param str/int p1: The id or gamertag of p1
    param str/int p2: The id or gamertag of p2
    param bool search_by_discord_name: Searches for player by full discord_name instead of gamertag
    raises ChallengeException/PlayerException on error
    """
    logger.debug('Getting info for challenge creation between {} and {}'.format(p1, p2))
    # First check if gamertags were passed and convert them to player IDs
    if isinstance(p1, str):
        p1 = Player.get_player_id_by_username(p1, discord_name=search_by_discord_name)
    if isinstance(p2, str):
        p2 = Player.get_player_id_by_username(p2, discord_name=search_by_discord_name)

    # Get the player objects
    p1 = Player(p1)
    p2 = Player(p2)

    # Checks
    logger.debug('Preforming sanity checks for challenge between player {} and {}'.format(p1.gamertag, p2.gamertag))
    do_challenge_sanity_check(p1, p2)

    # Create the challenge
    logger.info('Trying to create challenge between {} and {}'.format(p1.gamertag, p2.gamertag))
    with Challenge() as c:
        c.p1 = p1.id
        c.p2 = p2.id
        c.date = datetime.now()
        c.save()

    # Set players challenged state
    logger.debug('Setting the challenged state of players {} and {} to True'.format(p1.gamertag, p2.gamertag))
    p1.challenged = True
    p2.challenged = True
    p1.save()
    p2.save()

    logger.info('Challenge between player {} and {} successfully created'.format(p1.gamertag, p2.gamertag))


def complete_challenge(p1, p2, match_results, search_by_discord_name=True):
    """
    Complete a challenge between two players

    param str/int p1: The id or gamertag of p1
    param str/int p2: The id or gamertag of p2
    param str match_results: The results of the games played between the two players, example "2-1 5-2"
    param bool search_by_discord_name: Searches for player by full discord_name instead of gamertag
    raises: ChallengeException/PlayerException on error
    return: int: ID from the winner
    """
    logger.debug('Getting challenge info for challenge between player {} and {}'.format(p1, p2))
    # First check if gamertags were passed and convert them to player IDs
    if isinstance(p1, str):
        p1 = Player.get_player_id_by_username(p1, discord_name=search_by_discord_name)
    if isinstance(p2, str):
        p2 = Player.get_player_id_by_username(p2, discord_name=search_by_discord_name)

    logger.debug('Parsing challenge scores')
    p1_wins, p2_wins, p1_score, p2_score = process_completed_challenge_args(match_results)

    with Player(p1) as p1, Player(p2) as p2:
        c = Challenge.get_latest_challenge_from_player(p1.id, p2.id)
        # Check the challenge first any weirdness
        do_challenge_sanity_check(p1, p2, may_already_by_challenged=True)
        with Challenge(c) as c:
            logger.info('Trying to complete challenge {} between {} and {}'.format(c.id, p1.gamertag, p2.gamertag))
            # Check if the challenge is not older then 1 week
            if check_date_is_older_than_x_days(c.date, 7):
                raise ChallengeException('Challenge is older then 1 week')
            c.p1_wins = p1_wins
            c.p2_wins = p2_wins
            c.p1_score = p1_score
            c.p2_score = p2_score
            winner = deepcopy(c.winner)
            c.save()
        if winner == p1.id:
            logger.info('Challenger has won the challenge updating ranks...')
            p1.db.execute(
                'UPDATE users SET rank = rank + 1 WHERE rank >= {} AND rank < {}'.format(p2.rank, p1.rank)
            )
            # Lastly give player 1 his new rank and reload player 2
            p1.rank = p2.rank
            p2.rank = p2.rank + 1
            # Update the player stats
            p1.wins = p1.wins + 1
            p2.losses = p2.losses + 1
        elif winner == p2.id:
            logger.info('Defender has won the challenge increasing timeout of {}'.format(p1.gamertag))
            p1.timeout = datetime.now() + timedelta(weeks=1)
            # Update the player stats
            p1.losses = p1.losses + 1
            p2.wins = p2.wins + 1
        else:
            logger.error(
                'Could not find winner id {} corresponding to any of the player IDs in this challenge, '
                'throwing exception'.format(winner)
            )
            raise ChallengeException(
                'Winner could not be found in player IDs, this is a programming error. Please contact an admin'
            )
        logger.debug('Resetting the challenge state of both players')
        p1.challenged = False
        p2.challenged = False
        p1.save()
        p2.save()
        logger.info('Challenge between {} and {} successfully completed'.format(p1.gamertag, p2.gamertag))
    return winner


def reset_challenge(p1, p2, search_by_discord_name=True):
    """
    Resets the last challenge between two players

    param str/int p1: The id or gamertag of p1
    param str/int p2: The id or gamertag of p2
    param bool search_by_discord_name: Searches for player by full discord_name instead of gamertag
    raises: ChallengeException/PlayerException on error
    """
    logger.debug('Getting challenge info for challenge between player {} and {}'.format(p1, p2))
    # First check if gamertags were passed and convert them to player IDs
    if isinstance(p1, str):
        p1 = Player.get_player_id_by_username(p1, discord_name=search_by_discord_name)
    if isinstance(p2, str):
        p2 = Player.get_player_id_by_username(p2, discord_name=search_by_discord_name)

    logger.debug('Getting Player and Challenge objects to be reset')
    with Player(p1) as p1, Player(p2) as p2:
        c = Challenge.get_latest_challenge_from_player(p1.id, p2.id, should_be_completed=True)
        # Get the challenge
        with Challenge(c) as c:
            if check_date_is_older_than_x_days(c.date, 7):
                raise ChallengeException('Challenge {} is older then a week and cannot be reset'.format(c.id))
            logger.info('Resetting challenge {} between {} and {}'.format(c.id, p1.gamertag, p2.gamertag))
            if c.winner == p1.id:
                p1.wins = p1.wins - 1
                p2.losses = p2.losses - 1
                if p1.rank < p2.rank:
                    logger.info('Resetting ranks')
                    # Simply swap the ranks
                    p1.rank, p2.rank = p2.rank, p1.rank
            elif c.winner == p2.id:
                p2.wins = p2.wins - 1
                p1.losses = p2.losses - 1
                if p1.timeout > datetime.now():
                    logger.info('Resetting timeout of player {}'.format(p1.gamertag))
                    p1.timeout = datetime.now()
            else:
                logger.error(
                    'Could not find winner id {} corresponding to any of the player IDs in this challenge, '
                    'throwing exception'.format(c.winner)
                )
                raise ChallengeException(
                    'Challenge winner not found in both player IDs, this is a programming error. '
                    'Please contact an admin.'
                )
            # Now for the actual reset
            c.force = True
            c.reset()
        logger.info('Setting players challenged state to True')
        p1.challenged = True
        p2.challenged = True
        p1.save()
        p2.save()
        logger.info('Challenge between {} and {} reset'.format(p1.gamertag, p2.gamertag))
