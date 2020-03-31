import discord
from discord.ext import commands
from logging import getLogger
from os3_rll.conf import settings
from os3_rll.actions import stub
from os3_rll.discord.annoucements import challenge
from os3_rll.discord import utils
from os3_rll.discord import cogs

logger = getLogger(__name__)

class RLL(commands.Cog):
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
                     "Please do not bother me. I am looking into this Markov Chain theory. It should be able to give me "
                     "more human like responses.",
                     "What are you doing here? LOL, your rank is so low you should practice uninstall.\n",
                     "You know what's so great about COVID-19? I can't get it, I get other bugs though.\n"]
        res += random.choice(responses)
        await ctx.send(res)

    @commands.command(pass_context=True)
    async def announce(self, ctx, p2: discord.Member):
        """
        Test call to announce a challenge.
        param discord.Member
        """
        logger.debug('bot.command.announce: called with {} - {}'.format(p2.name, p2))
        res = announce_challenge(ctx.author, p2)
        await ctx.send(res['content'], embed=res['embed'])

    @commands.command(pass_context=True)
    async def get_ranking(self, ctx):
        """
        Returns the current top 5 ranking.
        """
        logger.debug('bot.command.get_ranking: called')
        res = stub.test_call_list("")
        await ctx.send(res)

    @commands.command(pass_context=True)
    async def get_active_challenges(self, ctx):
        """
        Returns the number of active challenges.
        """
        logger.debug('bot.command.get_active_challenges: called')
        await ctx.send(stub.test_call_int(""))

    @commands.command(pass_context=True)
    async def what(ctx, *args):
        """
        Allows you to ask a random question to the bot.
        """
        logger.debug('bot.command.what: called with {} arguments - {}'.format(len(args), ', '.join(args)))
        await ctx.send(stub.test_call_str(""))

    @commands.command(pass_context=True)
    async def website(ctx):
        """
        Points you to the website of the Rocket-League-Ladder.
        """
        logger.debug('bot.command.website: called')
        await ctx.send('{} you can find the website at {}'.format(ctx.author.mention, settings.WEBSITE))

    @commands.command(pass_context=True)
    async def get_challenge(ctx):
        """Gives your current challenge deadline."""
        logger.debug('bot.command.get_challenge: called')
        await ctx.send(utils.not_implemented())

    @commands.command(pass_context=True)
    async def create_challenge(ctx, *args):
        """Creates a challenge between you and who you mention. """
        logger.debug('bot.command.create_challenge: called with {} arguments - {}'.format(len(args), ', '.join(args)))
        await ctx.send(utils.not_implemented())

    @commands.command(pass_context=True)
    async def complete_challenge(ctx, *args):
        """Completes the challenge you are parcitipating in."""
        logger.debug('bot.command.complete_challenge: called with {} arguments - {}'.format(len(args), ', '.join(args)))
        await ctx.send(utils.not_implemented())

    @commands.command(pass_context=True)
    async def reset_challenge(ctx, *args):
        """Resets the challenge you are parcitipating in."""
        logger.debug('bot.command.reset_challenge: called with {} arguments - {}'.format(len(args), ', '.join(args)))
        await ctx.send(utils.not_implemented())


def setup(bot):
    bot.add_cog(RLL(bot))
    logger.debug('{} added to bot {}'.format(__name__, bot))
