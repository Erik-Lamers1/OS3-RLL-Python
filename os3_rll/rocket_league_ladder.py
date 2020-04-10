from argparse import ArgumentParser
from logging import INFO, DEBUG

from os3_rll.discord.client import discord_client
from os3_rll.log.log import setup_console_logging
from os3_rll.utils.version import show_version


def parse_args(args=None):
    parser = ArgumentParser(description="Rocket League Ladder program based on a Discord bot")
    parser.add_argument("-v", "--verbose", action="store_true", help="Display debug messages")
    parser.add_argument("-V", "--version", action="store_true", help="Show version and exit")
    return parser.parse_args(args)


def main(args=None):
    args = parse_args(args)
    if args.version:
        show_version()
        exit(0)
    setup_console_logging(verbosity=DEBUG if args.verbose else INFO)
    discord_client()


if __name__ == "__main__":
    main()
