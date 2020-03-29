from logging import getLogger
from os3_rll.models.db import Database
from os3_rll.actions.player import Player

logger = getLogger(__name__)


def process_challenge_data(p1, data):
    # Obtain the player 2 from the challenges database
    # SQL
    # "SELECT p2 FROM challenges WHERE p1={} AND winner = NULL SORT DESC LIMIT 1".format(p1.id)
    db = Database()
    db.execute('SELECT p2 FROM challenges WHERE p1="{}" AND winner = NULL SORT DESC'.format(p1.id))
    res = db.fetchone()
    # Except: no open challenges, someone fucked up.
    if res is None:
        raise Exception("No challenges available")

    # Get player gamertag by player ID and create an instance for player 2.
    p2 = Player(Player.get_gamertag_by_id(res[0]))
    scores = data.replace(':', '-').split(' ')
    # If p1_score > 0, p1 is the winner. If p1_score < 0, p2 is the winner.
    p1_score = 0
    try:
        for score in scores:
            s1, s2 = score.split('-')
            if s1 > s2:
                p1_score += 1
            if s1 < s2:
                p1_score -= 1
    except Exception:
        raise Exception("The score format is invalid. Please use the format: [$challenge_complete 0-1 2-3 4-5]")

    # Player 1 wins, clear timers
    if p1_score > 0:
        p1.clear_timeout()
        p2.clear_timeout()
    # Player 2 wins, only clear p2 timer
    if p1_score < 0:
        p2.clear_timeout()
    # Someone made an boo-boo
    if p1_score == 0:
        raise Exception("The match is a draw, please redo the match or enter the correct score")

