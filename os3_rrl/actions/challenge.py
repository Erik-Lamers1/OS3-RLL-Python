import time


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
        # 'INSERT INTO challenges (date, p1, p2) VALUES (NOW(), {}, {}).format(p1.id, p2.id)
        pass

    @staticmethod
    def announce_challenge(p1, p2):
        # Do discord magic
        pass

    # ####################################### #
    #  Methods when a challenge has completed #
    # ####################################### #

    @staticmethod
    def process_challenge_data(p1, data):
        # Obtain the player 2 from the challenges database
        # SQL
        # "SELECT p2 FROM challenges WHERE p1={} AND winner = NULL SORT DESC LIMIT 1".format(p1.id)
        # Except: no open challenges, someone fucked up.
        p2 = "p2"

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
            raise Exception("The score format is invalid. Please use the format: [0-1 2-3 4-5]")

        # Player 1 wins, clear timers
        if p1_score > 0:
            p1.clear_timer()
            p2.clear_timer()

        # Player 2 wins, only clear p2 timer
        if p1_score < 0:
            p2.clear_timer()

        # Someone made an boo-boo
        if p1_score == 0:
            raise Exception("The match is a draw, please redo the match or enter the correct score")

    @staticmethod
    def set_winner(challenge, player):
        pass

    @staticmethod
    def update_player_rank(player, r):
        # Update player rank += 1 WHERE rank >= r AND rank < player.rank
        # 'UPDATE users SET rank = rank + 1 WHERE rank >= {} AND rank < {}'.format(r, player.rank)

        # Update player.rank = r
        # 'UPDATE users SET rank={} WHERE id={player.id}'.format(r)
        pass
