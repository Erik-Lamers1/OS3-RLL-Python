import discord
from discord.ext import commands
from logging import getLogger
from os3_rll.actions.challenge import create_challenge, complete_challenge, get_challenge, reset_challenge
from os3_rll.actions.player import get_player_ranking, get_player_stats
from os3_rll.actions import stub
from os3_rll.discord.utils import not_implemented
from os3_rll.discord.announcements.challenge import announce_challenge, announce_challenge_info, announce_winner
from os3_rll.discord.announcements.player import announce_rankings, announce_stats
from os3_rll.operations.challenge import get_player_objects_from_challenge_info

logger = getLogger(__name__)


class RLL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def get_ranking(self, ctx):
        """
        Returns the current player ranking leaderboard.
        """
        logger.debug('get_ranking: called by'.format(ctx.message.author))
        rankings = get_player_ranking() # returns dict with {'gamertag':'rank'}
        announcement = announce_rankings(rankings)
        await ctx.send(announcement['content'], embed=announcement['embed'])

    @commands.command(pass_context=True)
    async def get_stats(self, ctx):
        """
        Returns the current player stats.
        """
        logger.debug('get_stats: called by'.format(ctx.message.author))
        stats = get_player_stats()
        announcement = announce_stats(stats)
        await ctx.send(announcement['content'], embed=announcement['embed'])

    @commands.command(pass_context=True)
    async def get_active_challenges(self, ctx):
        """
        Returns the number of active challenges.
        """
        logger.debug('get_active_challenges: called')
        await ctx.send(stub.test_call_int(""))

    @commands.command(pass_context=True)
    async def get_my_challenges(self, ctx):
        """Gives your current challenge deadline."""
        player = ctx.message.author.name + "#" + str(ctx.message.author.discriminator)
        logger.debug('get_challenge: called for player {}'.format(player))
        res = get_challenge(player)
        announcement = announce_challenge_info(res)
        await ctx.send(announcement['content'], embed=announcement['embed'])

    @commands.command(pass_context=True)
    async def create_challenge(self, ctx, p: discord.Member):
        """
        Creates a challenge between you and who you mention.
        param discord.Member
        """
        p1 = str(ctx.author.name + "#" + str(ctx.author.discriminator))
        p2 = str(p.name + "#" + str(p.discriminator))
        logger.debug('creating challenge between {} and {}'.format(p1, p2))
        create_challenge(p1, p2)
        announcement = announce_challenge(ctx.author, p)
        await ctx.send(announcement['content'], embed=announcement['embed'])

    @commands.command(pass_context=True)
    async def complete_challenge(self, ctx, match_results : str):
        """Completes the challenge you are parcitipating in."""
        requester = ctx.author.name + "#" + str(ctx.author.discriminator)
        logger.debug('complete_challenge requested by {}'.format(requester))
        challenger, defender = get_player_objects_from_challenge_info(requester)
        winner_id = complete_challenge(challenger.id, defender.id, match_results)
        announcement = announce_winner(challenger, defender, winner_id, match_results)
        await ctx.send(announcement['content'], embed=announcement['embed'])

    @commands.command(pass_context=True)
    async def reset_challenge(self, ctx, *args):
        """Resets the challenge you are parcitipating in."""
        logger.debug('reset challenge requested by {}'.format(str(ctx.author)))
        challenger, defender = get_player_objects_from_challenge_info(str(ctx.author), should_be_completed=True)
        res = get_challenge(str(ctx.author))
        reset_challenge(challenger.id, defender.id)
        announcement = announce_reset(res)
        await ctx.send(announcement['content'], embed=announcement['embed'])


def setup(bot):
    bot.add_cog(RLL(bot))
    logger.debug('{} added to bot {}'.format(__name__, bot.user))
