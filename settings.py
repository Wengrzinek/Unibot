# from template
import os

# The prefix that will be used to parse commands. Necessary but not needed here.
COMMAND_PREFIX = "!"

# The bot token. It's essentially the link between Discord and the bot. Keep it secret!
BOT_TOKEN = "ENTER BOT TOKEN HERE"

# The channel name. Set it to nothing to enable the bot in every channel
CHANNEL_NAME = ""

# The now playing game setting. Set this to anything or nothing to disable it
NOW_PLAYING = ""

# Base directory.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
