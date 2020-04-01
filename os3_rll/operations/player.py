from threading import Lock

from os3_rll.models.player import Player
from os3_rll.models.db import Database


def update_player_rank(player, rank):
    """
    Updates the rank of a player

    param int player: The id of the player to update the rank for
    param int rank: The new rank to give to the player
    """
    with Player(player) as p:
        p.rank = rank
        p.save()


def update_rank_of_player_cascading(player, rank):
    """
    Update the rank a of player to a new value.
    This will trigger a cascading update of all the player ranks below the new rank of <player>

    param int player: The id of the player to update the rank for
    param int rank: The new rank to give to the player
    """
    # This a an atomic operation, let's get a lock
    lock = Lock()
    with lock:

        # Check if we have duplicate ranks
        def _update_rank_of_player_cascading(p, r):
            update_player_rank(player, rank)
            with Database() as db:
                db.execute_prepared_statement('SELECT id, rank FROM users WHERE rank=%s AND id!=%s', (r, p))
                if db.rowcount < 1:
                    # All done
                    return
                else:
                    # Update the rank of the other player
                    other_player, other_rank = db.fetchone()
                    # Call myself with the other player and a rank 1 place lower
                    _update_rank_of_player_cascading(other_player, other_rank+1)

        _update_rank_of_player_cascading(player, rank)


