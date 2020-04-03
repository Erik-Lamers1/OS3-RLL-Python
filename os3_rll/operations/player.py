from threading import Lock
from logging import getLogger

from os3_rll.models.player import Player
from os3_rll.models.db import Database

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
