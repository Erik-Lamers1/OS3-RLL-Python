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


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def hi(self, ctx, *args):
        """Say hi to the bot, maybe it'll greet you nicely."""
        logger.debug('bot.command.hi: called with {} arguments - {}'.format(len(args), ', '.join(args)))
        res = 'Hi {}\n'.format(ctx.author.mention)
        responses = ["How are you doing today? Wait that's retorical, I am a bot I do not care.\n",
                     "I was just looking at your rank. Did you know that you suck at rocket league? I heard some guy "
                     "SquishyMuffinz is best.\n",
                     "Please leave me alone. I am randomizing the rankings database to mess with Mr.Vin.\n",
                     "Due to COVID-19 I've had to reimplement the transport protocol from QUIC to plain UDP to avoid "
                     "handshakes.\n",
                     "Please do not bother me. I am looking into this Markov Chain theory. It should be able to give "
                     "me "
                     "more human like responses.",
                     "What are you doing here? LOL, your rank is so low you should practice uninstall.\n",
                     "You know what's so great about COVID-19? I can't get it, I get other bugs though.\n"]
        res += random.choice(responses)
        await ctx.send(res)

    @commands.command(pass_context=True)
    async def what(self, ctx, *args):
        """
        Allows you to ask a random question to the bot.
        """
        logger.debug('bot.command.what: called with {} arguments - {}'.format(len(args), ', '.join(args)))
        await ctx.send(stub.test_call_str(""))

    @commands.command(pass_context=True)
    async def announce_challenge(self, ctx, p: discord.Member):
        """
        Test call to announce a challenge. This does nothing with the database. It just makes the bot post Bullshit.
        param discord.Member
        """
        announcement = announcements.challenge.announce_challenge(ctx.author, p)
        await ctx.send(announcement['content'], embed=announcement['embed'])


    #@commands.command(pass_context=True)
    #async def announce_rankings(self, ctx)
    #announcement = announcements.rankings.announce_rankings()

    @commands.command(pass_context=True)
    async def debug_reset_challenge(self, ctx, *args):
        """Resets the challenge you are parcitipating in."""
        logger.debug('bot.command.reset_challenge: called with {} arguments - {}'.format(len(args), ', '.join(args)))
        await ctx.send(not_implemented())


def setup(bot):
    bot.add_cog(Debug(bot))
    logger.debug('{} added to bot {}'.format(__name__, bot.user))
