import time
from logging import getLogger
from os3_rll.mysql.db import Database
from os3_rll.actions.player import Player
from os3_rll.discord import client

logger = getLogger(__name__)

db = Database()


class Challenge:

    # ############################# #
    # Methods to create a challenge #
    # ############################# #

    @staticmethod
    def do_player_sanity_check(p1, p2):
        if p1.challenged:
            raise Exception('{} is already challenged'.format(p1))

        if p2.challenged:
            raise Exception('{} is already challenged'.format(p2))

        # Check if the rank of player 1 is lower than the rank of player 2:
        if p1.rank < p2.rank:
            raise Exception('The rank of {} is lower than of {}'.format(p1, p2))

        # Check if the ranks are the same; this should not happen
        if p1.rank == p2.rank:
            raise Exception("The ranks of both players are the same. This should not happen. EVERYBODY PANIC!!!")

        # Check if the timeout of player 1 has expired
        if p1.timeout > int(time.time()):
            raise Exception("The timeout counter of {} is still active".format(p1))

    @staticmethod
    def create_challenge_entry(p1, p2):
        db.execute('INSERT INTO challenges (date, p1, p2) VALUES (NOW(), {}, {})'.format(p1.id, p2.id))

    @staticmethod
    def announce_challenge(players):
        """Generates an announcement to be posted by the discord bot as an embed

           Params:
               players: (list of players)
               p1: player1 (the challenger) its discord name.
               p2: player2 (the challengee) its discord name.

           return:
               Dictionary with content, title, description, footer and colour as keys.
        """
        # Get the mentions of the players. Raises a TypeError if it cannot find the players
        try:
            p1 = players[0]
            p2 = players[1]
            challenger, challengee = client.get_player_mentions(p1, p2)
            message = {'content':"New Challenge!",
                       'title':"**{} challenges {}.**".format(challenger, challengee),
                       'description':"This match should be played within one week or {} wins automatically.".format(challenger),
                       'footer':"Good Luck!",
                       'colour':"2234352"}

            client.post_embed(message)
        except TypeError:
            logger.error("actions.challenge.announce_challenge: Found NoneType Object for {} or {}".format(p1, p2))



    # ####################################### #
    #  Methods when a challenge has completed #
    # ####################################### #

    @staticmethod
    def process_challenge_data(p1, data):
        # Obtain the player 2 from the challenges database
        # SQL
        # "SELECT p2 FROM challenges WHERE p1={} AND winner = NULL SORT DESC LIMIT 1".format(p1.id)
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

    @staticmethod
    def set_winner(challenge, player):
        pass

    @staticmethod
    def update_player_rank(player, r):
        """
        Updates the rank of the player to the new rank r. All player ranks between the old and new rank are increased
        by 1.
        :param player: The Player object
        :param r: The new rank of the player
        """
        # 'UPDATE users SET rank = rank + 1 WHERE rank >= {} AND rank < {}'.format(r, player.rank)
        db.execute('UPDATE users SET rank = rank + 1 WHERE rank >= {} AND rank < {}'.format(r, player.rank))

        # Update player.rank = r
        db.execute('UPDATE users SET rank={} WHERE id={}'.format(r, player.id))

    # ################################# #
    #  Methods for challenge management #
    # ################################# #

    @staticmethod
    def get_challenge(args):
        """
        Return the outstanding challenge of the requesting player, if any.
        :type args: Player ID
        """
        logger.debug('actions.challenge.Challenge.get_challenge: called with {}'.format(args))
        # Get the player ID
        pid = Player.get_id_by_gamertag(args[0].name)
        logger.debug('actions.challenge.Challenge.get_challenge: found player {} with id {}'.format(args[0].name, pid))

        db.execute('SELECT date, p1, p2 FROM challenges WHERE p1 = "{}" AND winner IS NULL'.format(pid))
        res = db.fetchone()
        logger.debug('actions.challenge.Challenge.get_challenge: got database result: {}'.format(res))

        if res is None:
            return "No outstanding challenges for player {} with pid {} found.".format(args[0].name, pid)
        else:
            return "A challenge is active until {} between {} and {}".format(res[0], res[1], res[2])

    @staticmethod
    def get_all_challenges():
        # Return all challenges
        pass

    @staticmethod
    def get_active_challenges():
        pass

