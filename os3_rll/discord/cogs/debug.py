import discord
import random
import base64
from discord.ext import commands
from logging import getLogger
from os3_rll.conf import settings
from os3_rll.actions.challenge import create_challenge, complete_challenge
from os3_rll.actions import stub
from os3_rll.discord.utils import not_implemented
from os3_rll.discord.announcements import challenge
from os3_rll.operations.challenge import get_player_objects_from_challenge_info

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
        announcement = challenge.announce_challenge(ctx.author, p)
        await ctx.send(announcement['content'], embed=announcement['embed'])


    #@commands.command(pass_context=True)
    #async def announce_rankings(self, ctx)
    #announcement = announcements.rankings.announce_rankings()

    @commands.command(pass_context=True)
    async def debug_reset_challenge(self, ctx, *args):
        """Resets the challenge you are parcitipating in."""
        logger.debug('bot.command.reset_challenge: called with {} arguments - {}'.format(len(args), ', '.join(args)))
        await ctx.send(not_implemented())


    @commands.command(pass_context=True, hidden=True)
    async def i_choose_you(self, ctx):
        """Whut?... It's super effective."""
        n25 = ('ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLC0u'
            'CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIF8ufCAg'
            'JwogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLicgIHwg'
            'LwogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICwnICAgIHwn'
            'CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAvICAgICAgLwog'
            'ICAgICAgICAgICAgICAgICAgICAgIF8uLi0tLS0iIi0tLS4nICAgICAgLwogXy4u'
            'Li4uLS0tLS0tLS0tLi4uLC0iIiAgICAgICAgICAgICAgICAgICwnCiBgLS5fICBc'
            'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAvCiAgICAgYC0uK18gICAg'
            'ICAgICAgICBfXyAgICAgICAgICAgLC0tLiAuCiAgICAgICAgICBgLS4uXyAgICAg'
            'LjogICkuICAgICAgICAoYC0tInwgXAogICAgICAgICAgICAgICA3ICAgIHwgYCIg'
            'fCAgICAgICAgIGAuLi4nICBcCiAgICAgICAgICAgICAgIHwgICAgIGAtLScgICAg'
            'ICcrIiAgICAgICAgLCIuICwiIi0KICAgICAgICAgICAgICAgfCAgIF8uLi4gICAg'
            'ICAgIC5fX19fICAgICB8IHwvICAgICcKICAgICAgICAgIF8uICAgfCAgLiAgICBg'
            'LiAgJy0tIiAgIC8gICAgICBgLi8gICAgIGoKICAgICAgICAgXCcgYC0ufCAgJyAg'
            'ICAgfCAgIGAuICAgLyAgICAgICAgLyAgICAgLwogICAgICAgICAnICAgICBgLS4g'
            'YC0tLSIgICAgICBgLSIgICAgICAgIC8gICAgIC8KICAgICAgICAgIFwgICAgICAg'
            'YC4gICAgICAgICAgICAgICAgICBfLCcgICAgIC8KICAgICAgICAgICBcICAgICAg'
            'ICBgICAgICAgICAgICAgICAgICAgICAgICAgLgogICAgICAgICAgICBcICAgICAg'
            'ICAgICAgICAgICAgICAgICAgICAgICAgICBqCiAgICAgICAgICAgICBcICAgICAg'
            'ICAgICAgICAgICAgICAgICAgICAgICAgLwogICAgICAgICAgICAgIGAuICAgICAg'
            'ICAgICAgICAgICAgICAgICAgICAgLgogICAgICAgICAgICAgICAgKyAgICAgICAg'
            'ICAgICAgICAgICAgICAgICAgXAogICAgICAgICAgICAgICAgfCAgICAgICAgICAg'
            'ICAgICAgICAgICAgICAgIEwKICAgICAgICAgICAgICAgIHwgICAgICAgICAgICAg'
            'ICAgICAgICAgICAgICB8CiAgICAgICAgICAgICAgICB8ICBfIC8sICAgICAgICAg'
            'ICAgICAgICAgICAgfAogICAgICAgICAgICAgICAgfCB8IEwpJy4uICAgICAgICAg'
            'ICAgICAgICAgIHwKICAgICAgICAgICAgICAgIHwgLiAgICB8IGAgICAgICAgICAg'
            'ICAgICAgICB8CiAgICAgICAgICAgICAgICAnICBcJyAgIEwgICAgICAgICAgICAg'
            'ICAgICAgJwogICAgICAgICAgICAgICAgIFwgIFwgICB8ICAgICAgICAgICAgICAg'
            'ICAgagogICAgICAgICAgICAgICAgICBgLiBgX18nICAgICAgICAgICAgICAgICAv'
            'CiAgICAgICAgICAgICAgICBfLC4tLS4tLS0uLi4uLi4uLl9fICAgICAgLwogICAg'
            'ICAgICAgICAgICAtLS0uLCctLS1gICAgICAgICAgfCAgIC1qIgogICAgICAgICAg'
            'ICAgICAgLi0nICAnLi4uLl9fICAgICAgTCAgICB8CiAgICAgICAgICAgICAgIiIt'
            'LS4uICAgIF8sLScgICAgICAgXCBsfHwKICAgICAgICAgICAgICAgICAgLC0nICAu'
            'Li4uLi0tLS0tLS4gYHx8JwogICAgICAgICAgICAgICBfLCcgICAgICAgICAgICAg'
            'ICAgLwogICAgICAgICAgICAgLCcgICAgICAgICAgICAgICAgICAvCiAgICAgICAg'
            'ICAgICctLS0tLS0tLS0rLSAgICAgICAgLwogICAgICAgICAgICAgICAgICAgICAv'
            'ICAgICAgICAgLwogICAgICAgICAgICAgICAgICAgLicgICAgICAgICAvCiAgICAg'
            'ICAgICAgICAgICAgLicgICAgICAgICAgLwogICAgICAgICAgICAgICAsJyAgICAg'
            'ICAgICAgLwogICAgICAgICAgICAgXycuLi4uLS0tLSIiIiIiIG1o')
        pokeball = '```{}```'.format(str(base64.b64decode(n25), "ascii"))
        await ctx.send(pokeball)


def setup(bot):
    bot.add_cog(Debug(bot))
    logger.debug('{} added to bot {}'.format(__name__, bot.user))
