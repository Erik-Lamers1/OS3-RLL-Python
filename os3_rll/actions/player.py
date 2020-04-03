from logging import getLogger

from os3_rll.models.db import Database, DBException

logger = getLogger(__name__)


def get_player_ranking():
    """
    Gets the current player ranking from the DB

    returns dict: {str discord: int rank, ...}
    """
    players = {}
    logger.info('Getting current player ranking from DB')
    with Database() as db:
        db.execute('SELECT discord, rank FROM users WHERE rank > 0 ORDER BY rank')
        if db.rowcount == 0:
            raise DBException('No players found')
        rows = db.fetchall()
        for row in rows:
            # Fill the dict with discord => rank
            players[row[0]] = row[1]
    return players
