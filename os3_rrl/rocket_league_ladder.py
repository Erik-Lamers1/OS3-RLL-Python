from argparse import ArgumentParser
from logging import INFO, DEBUG

from os3_rrl.discord.client import discord_client
from os3_rrl.logging.log import setup_console_logging


def main(args=None):
    parser = ArgumentParser(description='Rocket League Ladder program based on a Discord bot')
    parser.add_argument('-v', '--verbose', action='store_true', help='Display debug messages')
    args = parser.parse_args(args)
    setup_console_logging(verbosity=DEBUG if args.verbose else INFO)
    discord_client()


if __name__ == '__main__':
    main()
