import discord
import random
import re
from discord.ext import commands
from logging import getLogger
from os3_rll.actions import stub
from os3_rll.discord.utils import not_implemented
from os3_rll.discord.announcements import challenge
from os3_rll.discord.pokedex import Pokedex

logger = getLogger(__name__)


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dex = Pokedex()

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
                     "You know what's so great about COVID-19? I can't get it, I get other bugs though.\n",
                     "Do you sometimes have those games where you fail to make every pass, every save, every clear, every shot, every assist? Well it's probably because Mr. Vin is in your team. For a straight guy he sure likes to chase balls.\n",
                     "Did you ever play a rocket league match where you team mate chokes up in front of the opposite goal when he is supposed to score? Well then you must have been playing with toekel.\n",
                     "Did you hear from SyntheticOxygen? No? Well then he must still be stuck in Silver III.\n",
                     "Did you see your team mate ever make a save? No? Well then you must have been playing with Pandabeer.\n"]
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

    @commands.command(pass_context=True)
    async def debug_reset_challenge(self, ctx, *args):
        """Resets the challenge you are parcitipating in."""
        logger.debug('bot.command.reset_challenge: called with {} arguments - {}'.format(len(args), ', '.join(args)))
        await ctx.send(not_implemented())

    @commands.command(pass_context=True, hidden=True)
    async def i_choose_you(self, ctx, pokemon: str=""):
        """Whut?... It's super effective.
           params: a string to parse defaults to empty
                   ""          -> chooses random pokemon and random art
                   "pikachu"   -> returns pikachu asciiart
                   "25"        -> returns pikachu
                   "25 1"      -> returns pikachu with alternative ascii art
                   "pikachu 1" -> returns pikachu with alternative ascii art
                   "pikachu rnd" -> returns pikachu with random ascii art
                   "25 rnd" -> returns pikachu with random ascii art"
        """
        pokeball = ""

        if pokemon == "":
            poke_id = random.choice(self.dex.list_pokemons())[0]
            pokeball = self.dex.choose_by_id(poke_id, rnd=True)
        else:
            if int(pokemon) in range(0, 152):
                logger.debug('bot.i_choose_you: called with id: {}'.format(pokemon))
                pokeball = self.dex.choose_by_id(int(pokemon), rnd=True)
            else:
                logger.debug('bot.i_choose_you: called with name: {}'.format(pokemon))
                pokeball = self.dex.choose_by_name(str(pokemon), rnd=False)

        msg = '```{}```'.format(pokeball)
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Debug(bot))
    logger.debug('{} added to bot {}'.format(__name__, bot.user))
