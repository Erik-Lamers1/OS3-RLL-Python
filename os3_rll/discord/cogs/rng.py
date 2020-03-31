import random
from discord.ext import commands

class RNG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def roll(self, ctx, dice: str):
        """
        Rolls a dice in NdN format.
        param str NdN
        ---
        N stands for the amount of dice to be thrown
        d is the separator
        N is the amount of sides on a dice.
        For example 5d6 would throw 5 6-siced dice.
        """
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send("Format has to be in NdN!")

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(pass_context=True, description='For when you wanna settle the score some other way')
    async def choose (self, ctx, *choices : str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))


def setup(bot):
    logger.debug('{}: added to bot {}'.format(__name__, bot))
    bot.add_cog(RNG(bot))
