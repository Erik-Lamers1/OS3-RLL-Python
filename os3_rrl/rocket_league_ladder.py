from os3_rrl.discord.client import discord_client
from os3_rrl.logging.log import setup_console_logging


def main():
    setup_console_logging()
    discord_client()


if __name__ == '__main__':
    main()
