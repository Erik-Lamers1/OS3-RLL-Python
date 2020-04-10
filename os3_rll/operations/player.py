from logging import getLogger

from os3_rll.models.db import Database, DBException

logger = getLogger(__name__)


def get_all_player_ids_ordered(order_by="rank"):
    """
    Get a list of all player ids ordered by column

    param str order_by: Which column to order by
    return list: The player ids
    """
    ids = []
    with Database() as db:
        db.execute_prepared_statement("SELECT id FROM users ORDER BY %s", (order_by,))
        if db.rowcount == 0:
            raise DBException("No users returned")
        rows = db.fetchall()
        for row in rows:
            ids.append(row[0])
    return ids


def get_average_goals_per_challenge(player):
    """
    Gets the average goals per challenge for a player

    param int player: The player id to get the average goals for
    return int: The average goals per challenge
    """
    logger.debug("Calculating average goals per challenge for player with id {}".format(player))
    with Database() as db:
        # Average goals as p1
        db.execute_prepared_statement("SELECT AVG(p1_score) FROM challenges WHERE p1=%s AND WINNER IS NOT NULL", (player,))
        if db.rowcount != 1:
            logger.warning("Player with id {} has never challenged someone, setting average challenger score to 0")
            avg_challenger_score = 0
        else:
            avg_challenger_score = db.fetchone()[0]
            # If the player has never scored this variable will be None
            if avg_challenger_score is None:
                avg_challenger_score = 0
        # Average goals as p2
        db.execute_prepared_statement("SELECT AVG(p2_score) FROM challenges WHERE p2=%s AND WINNER IS NOT NULL", (player,))
        if db.rowcount != 1:
            logger.warning("Player with id {} has never been challenged, setting average challenged score to 0")
            avg_challenged_score = 0
        else:
            avg_challenged_score = db.fetchone()[0]
            # If the player has never scored this variable will be None
            if avg_challenged_score is None:
                avg_challenged_score = 0
    # Return the average of the two numbers
    return float(avg_challenger_score) + float(avg_challenged_score) / 2
