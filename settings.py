# from template
import os

# The prefix that will be used to parse commands.
# It doesn't have to be a single character!
COMMAND_PREFIX = "!"

# The bot token. Keep this secret!
BOT_TOKEN = "ODEwNjA2ODIzMzA3NzM5MTc2.YCmGbw.NNvoDwgCLqL1y-mqU-gKOpOQs_E"

# The channel name. Set it to nothing to enable the bot in every channel
CHANNEL_NAME = "bot-1"  # bot-1 will be the default bot channel

# The now playing game. Set this to anything false-y ("", None) to disable it
NOW_PLAYING = ""

# Base directory. Feel free to use it if you want.
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
