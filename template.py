# Initial template, to be used for reference


# rocket league ladder bot
from os3_rll import discord
from os import getenv
from subprocess import check_output
from dotenv import load_dotenv
from logging import getLogger

logger = getLogger(__name__)

load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
GUILD = getenv("DISCORD_GUILD")
CHANNEL = getenv("DISCORD_CHANNEL")

php_cmd = ["php", "-f", "send_ranking.php"]

client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f"{client.user} is connected to the following guild:\n" f"{guild.name}(id: {guild.id})")


@client.event
async def on_message(message):
    logger.debug("saw a message: {}".format(message))
    if message.channel.name == CHANNEL:
        if message.content.startswith("$get_ranking"):
            result = check_output(php_cmd).decode("utf-8")
            await client.send_message(message.channel, result)


while True:
    client.run(TOKEN)
