import discord
import re
from discord.ext import commands
from logging import getLogger
from os3_rll.actions.player import add_player, reset_player_password

# from os3_rll.discord.announcements.challenge import announce_new_season
from os3_rll.discord.announcements.player import announce_new_player
from os3_rll.discord.client import is_rll_admin
from os3_rll.discord.utils import get_player, not_implemented
from os3_rll.conf import settings

logger = getLogger(__name__)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ps_regex = re.compile(r"^(.{1,32}#\d{4})\s+(.+)\s+(.+)$")

    @commands.command(pass_context=True)
    @is_rll_admin()
    async def start_new_season(self, ctx):
        """Resets the player ranking, scrambles a new leader bord, but keeps player statistics."""
        logger.debug("start_new_seasion requested by {}".format(str(ctx.author)))
        # announcement = announce_new_season(res)
        # await ctx.send(announcement["content"], embed=announcement["embed"])
        await ctx.send(not_implemented())

    @commands.command(pass_context=True)
    @is_rll_admin()
    async def add_player(self, ctx, player: discord.Member, *player_settings):
        """Allows RLL Admins to add players to the Rocket League Ladder.
           Players need a gamertag, discord handle and a name
        """
        logger.info("add_player: called by {} for {}".format(ctx.author, str(player)))
        argument_string = "{} {}".format(str(player), " ".join(player_settings))
        input_match = self.ps_regex.fullmatch(argument_string)
        if not input_match:
            input_err_msg = (
                "Wrong arguments given.\n" + "Expected: <@DiscordMention> <name> <gamertag>\n" + "Got: {}\n".format(player_settings)
            )
            raise commands.UserInputError(input_err_msg)
        if get_player(str(player)) is None:
            raise commands.BadArgument("{} is not a member of this guild.".format(str(player)))

        name, gamertag = input_match.group(2, 3)
        player_info, password = add_player(name, gamertag, str(player))
        logger.info("Player successfully created")
        # TODO: Bug below this line
        # TypeError:  'Player' object is not subscriptable
        # Using below method is buggy and not recommended, stupid documentation
        # fixed in line 63 and 64
        # player_channel = await player.create_dm()
        # admin_channel = await ctx.author.create_dm()
        admin_msg = "Created player for {p.name} with gamertag: {p.gamertag} and discord {p.discord}.".format(p=player_info)
        player_msg = (
            "{} has created an account for you your login username is {}, "
            "your password is {} please change this password at {} ASAP.".format(
                str(ctx.author), player_info.gamertag, password, settings.WEBSITE
            )
        )
        await ctx.author.send(admin_msg)
        await player.send(player_msg)
        logger.debug("Announcing new player info to channel")
        announcement = announce_new_player(player_info)
        await ctx.send(announcement["content"], embed=announcement["embed"])

    @commands.command(pass_context=True)
    @is_rll_admin()
    async def reset_password(self, ctx, player: discord.Member):
        """
        Allows RLL Admins to reset a players password.
        The bot will send the password via DM to the player.
        Params:
            discord.Member -> a discord member, can be a username string or a mention or an id etc, discord.py api handles this.
            Returns DM with password to player, and a success message to the channel.
        """
        logger.debug("reset_password: called by {} for {}".format(ctx.author, str(player)))
        if get_player(str(player)) is None:
            raise commands.BadArgument("{} is not a member of this guild.".format(str(player)))

        password = reset_player_password(str(player), discord_name=True)
        player_channel = await player.create_dm()
        msg = "Reset password for player for {}".format(str(player))
        player_msg = "{} has reset your password your new password is {} please change this password at {} ASAP.".format(
            str(ctx.author), password, settings.WEBSITE
        )
        await player_channel.send(player_msg)
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(Admin(bot))
    logger.debug("{} added to bot {}".format(__name__, bot.user))
