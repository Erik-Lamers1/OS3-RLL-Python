import discord
from discord.ext import commands
from logging import getLogger

logger = getLogger(__name__)


class Members(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        await ctx.send("{0.name} joined in {0.joined_at}".format(member))

    @commands.group(pass_context=True)
    async def cool(self, ctx):
        """
        Says if a user is cool.

        In reality this just checks if a subcommand is being invoked.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("No, {0.subcommand_passed} is not cool.".format(ctx))

    @cool.command(pass_context=True, name="bot")
    async def _bot(self, ctx):
        """
        Is the bot cool?
        """
        await ctx.send("Yes, I am cool.")

    @cool.command(pass_context=True, name="Mr. Vin")
    async def _mr_vin(self, ctx):
        """
        Is Mr. Vin cool?
        """
        await ctx.send("No, Mr. Vin is not cool, he is a lazy f*ck.")

    @cool.command(pass_context=True, name="SyntheticOxygen")
    async def _syntheticoxygen(self, ctx):
        """
        Is SyntheticOxygen cool?
        """
        await ctx.send("Yes, SyntheticOxygen is cool, because he is my developer.")

    @cool.command(pass_context=True, name="Pandabeer")
    async def _pandabeer(self, ctx):
        """
        Is Pandabeer cool?
        """
        await ctx.send("Yes, Pandabeer is cool, because he is my developer.")

    @cool.command(pass_context=True, name="wilmar446")
    async def _wilmar446(self, ctx):
        """
        Is wilmar446 cool?
        """
        await ctx.send("No, that motherfucker is just a toxic asshole.")


def setup(bot):
    bot.add_cog(Members(bot))
    logger.debug("{} added to bot {}".format(__name__, bot.user))
