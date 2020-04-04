from threading import Lock
from logging import getLogger

from os3_rll.models.player import Player, PlayerException
from os3_rll.models.db import Database, DBException

logger = getLogger(__name__)


def update_player_rank(player, rank):
    """
    Updates the rank of a player

    param int player: The id of the player to update the rank for
    param int rank: The new rank to give to the player
    """
    logger.info('Updating rank op player with id {} to {}'.format(player, rank))
    with Player(player) as p:
        p.rank = rank
        p.save()


def update_rank_of_player_cascading(player1, player2):
    """
    Update the rank a of player to a new value.
    This will trigger a cascading update of all the player ranks below the new rank of <player>

    param os3_rll.models.player.Player: Player model of player 1
    param os3_rll.models.player.Player: Player model of player 2
    """
    # This a an atomic operation, let's get a lock
    lock = Lock()
    with lock:

        # Check if we have duplicate ranks
        def _update_rank_of_player_cascading(p1, p2, save=False):
            p1.rank = p2.rank
            with Database() as db:
                db.execute_prepared_statement('SELECT id FROM users WHERE rank=%s AND id!=%s', (p1.rank, p1.id))
                if db.rowcount < 1:
                    if save:
                        p1.save()
                        p2.save()
                    # All done
                    return
                else:
                    # Update the rank of the other player
                    other_player = db.fetchone()
                    other_player = Player(other_player)
                    # Call myself with the other player and a rank 1 place lower
                    _update_rank_of_player_cascading(other_player, other_rank+1)

        _update_rank_of_player_cascading(player1, player2)


def get_all_player_ids_ordered(order_by='rank'):
    """
    Get a list of all player ids ordered by column

    param str order_by: Which column to order by
    return list: The player ids
    """
    ids = []
    with Database() as db:
        db.execute_prepared_statement('SELECT id FROM users ORDER BY %s', (order_by,))
        if db.rowcount == 0:
            raise DBException('No users returned')
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
    logger.debug('Calculating average goals per challenge for player with id {}'.format(player))
    with Database() as db:
        # Average goals as p1
        db.execute_prepared_statement(
            'SELECT AVG(p1_score) FROM challenges WHERE p1=%s AND WINNER IS NOT NULL', (player,)
        )
        if db.rowcount != 1:
            logger.warning('Player with id {} has never challenged someone, setting average challenger score to 0')
            avg_challenger_score = 0
        else:
            avg_challenger_score = db.fetchone()[0]
            # If the player has never scored this variable will be None
            if avg_challenger_score is None:
                avg_challenger_score = 0
        # Average goals as p2
        db.execute_prepared_statement(
            'SELECT AVG(p2_score) FROM challenges WHERE p2=%s AND WINNER IS NOT NULL', (player,)
        )
        if db.rowcount != 1:
            logger.warning('Player with id {} has never been challenged, setting average challenged score to 0')
            avg_challenged_score = 0
        else:
            avg_challenged_score = db.fetchone()[0]
            # If the player has never scored this variable will be None
            if avg_challenged_score is None:
                avg_challenged_score = 0
    # Return the average of the two numbers
    return float(avg_challenger_score) + float(avg_challenged_score) / 2
