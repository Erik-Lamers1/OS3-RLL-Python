from logging import getLogger
from datetime import datetime

from os3_rll.models.player import Player
from os3_rll.models.challenge import Challenge
from os3_rll.operations.challenge import do_challenge_sanity_check

logger = getLogger(__name__)


def create_challenge(p1, p2):
    """
    Create a challenge between p1 and p2. Where p1 is the one challenging and p2 is the one defending

    param str/int p1: The id or gamertag of p1
    param str/int p2: The id or gamertag of p2
    returns None if challenge successfully created
    raises ChallengeException/PlayerException on error
    """
    logger.debug('Getting info for challenge creation between {} and {}'.format(p1, p2))
    # First check if gamertags were passed and convert them to player IDs
    if isinstance(p1, str):
        p1 = Player.get_player_id_by_gamertag(p1)
    if isinstance(p2, str):
        p2 = Player.get_player_id_by_gamertag(p2)

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
