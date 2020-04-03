import discord
import random
from discord.ext import commands
from logging import getLogger
from os3_rll.conf import settings
from os3_rll.actions.challenge import create_challenge, complete_challenge
from os3_rll.actions import stub
from os3_rll.discord.utils import not_implemented
from os3_rll.discord import annoucements
from os3_rll.operations.challenge import get_player_objects_from_complete_challenge_info

logger = getLogger(__name__)


class RLL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def get_ranking(self, ctx):
        """
        Returns the current top 5 ranking.
        """
        logger.debug('called')
        res = stub.test_call_list("")
        await ctx.send(res)

    @commands.command(pass_context=True)
    async def get_active_challenges(self, ctx):
        """
        Returns the number of active challenges.
        """
        logger.debug('called')
        await ctx.send(stub.test_call_int(""))

    @commands.command(pass_context=True)
    async def get_challenge(self, ctx):
        """Gives your current challenge deadline."""
        logger.debug('called')
        await ctx.send(utils.not_implemented())

    @commands.command(pass_context=True)
    async def create_challenge(self, ctx, p: discord.Member):
        """
        Creates a challenge between you and who you mention.
        param discord.Member
        """
        p1 = str(ctx.author.name + "#" + str(ctx.author.discriminator))
        p2 = str(p.name + "#" + str(p.discriminator))
        logger.debug('creating challenge between {} and {}'.format(p1, p2))
        challenge.create_challenge(ctx.author, p2)
        announcement = announcements.challenge.announce_challenge(ctx.author, p)
        await ctx.send(announcement['content'], embed=announcement['embed'])

    @commands.command(pass_context=True)
    async def complete_challenge(self, ctx, match_results : str):
        """Completes the challenge you are parcitipating in."""
        requester = ctx.author.name + "#" + str(ctx.author.discriminator)
        logger.debug('complete_challenge requested by {}'.format(requester))
        challenger, defender = get_player_objects_from_complete_challenge_info(requester)
        winner_id = complete_challenge(challenger, defender, match_results)
        name = None
        disc = None
        if challenger.id == winner_id:
            name, disc = challenger.discord.split('#')
        elif defender.id == winner_id:
            name, disc = defender.discord.split('#')
        else:
            raise ValueError
        winner = discord.utils.get(ctx.message.channel.guild_members, name=name, discriminator=disc)
        announcement = announcement.challenger.announce_winner()
        await ctx.send(announcement['content'], embed=announcement['embed'])

    @commands.command(pass_context=True)
    async def reset_challenge(self, ctx, *args):
        """Resets the challenge you are parcitipating in."""
        logger.debug('called with {} arguments - {}'.format(len(args), ', '.join(args)))
        await ctx.send(utils.not_implemented())


def setup(bot):
    bot.add_cog(RLL(bot))
    logger.debug('{} added to bot {}'.format(__name__, bot.user))
