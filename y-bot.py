# from template
import sys
import aiml
import settings
import discord
import message_handler
import asyncio
import random
import wikipedia


from apscheduler.schedulers.asyncio import AsyncIOScheduler
from events.base_event import BaseEvent
from events import *
from multiprocessing import Process
from discord.ext.commands import Bot

# Set to remember if the bot is already running, since on_ready may be called
# more than once on reconnects
this = sys.modules[__name__]
this.running = False

# Scheduler that will be used to manage events
sched = AsyncIOScheduler()


###############################################################################

def main():
    # Initialize the client
    print("Starting up...")
    client = discord.Client()

    # AIML startup
    kernel = aiml.Kernel()
    kernel.learn("learn-startup.xml")
    kernel.respond("LOAD AIML")

    # Wikipeida init - Set language to German
    wikipedia.set_lang("de")

    bot = Bot('!')

    # Define event handlers for the client
    # on_ready may be called multiple times in the event of a reconnect,
    # hence the running flag

    @bot.command()
    async def test(ctx):
        await ctx.send("This is tts", tts=True)

    @client.event
    async def on_ready():
        if this.running:
            return

        this.running = True

        # Set the playing status
        if settings.NOW_PLAYING:
            print("Setting NP game", flush=True)
            await client.change_presence(
                activity=discord.Game(name=settings.NOW_PLAYING))
        print("Logged in!", flush=True)

        # Load all events
        print("Loading events...", flush=True)
        n_ev = 0
        for ev in BaseEvent.__subclasses__():
            event = ev()
            sched.add_job(event.run, 'interval', (client,),
                          minutes=event.interval_minutes)
            n_ev += 1
        sched.start()
        print(f"{n_ev} events loaded", flush=True)

    # The message handler for both new message and edits
    async def common_handle_message(message):
        text = message.content
        if text.startswith(settings.COMMAND_PREFIX) and text != settings.COMMAND_PREFIX:
            cmd_split = text[len(settings.COMMAND_PREFIX):].split()
            try:
                await message_handler.handle_command(cmd_split[0].lower(),
                                                     cmd_split[1:], message, client)
            except:
                print("Error while handling message", flush=True)
                raise

    # from https://towardsdatascience.com/how-to-build-your-own-ai-chatbot-on-discord-c6b3468189f4
    # and https://github.com/Assassinumz/Animus/
    @client.event
    async def on_message(message):
        channel = message.channel
        if message.author.bot or str(message.channel) != settings.CHANNEL_NAME:
            return

        if message.author == client.user:
            return

        if message.content is None:
            return

        if kernel.respond(message.content) == "s":
            return

        if "Y_QUERY" in kernel.respond(message.content):
            msg = message.content
            query = msg[8:]
            print(query)
            try:
                await channel.send("Okay, ich habe das Folgende dazu auf Wikipedia gefunden: ")
                response = wikipedia.summary(query)
                await channel.send(response)
                return
            except wikipedia.DisambiguationError as e:
                # await channel.send("Okay, ich habe das Folgende dazu auf Wikipedia gefunden: ")
                await channel.send(wikipedia.summary(e.options[0]))
                return
            except wikipedia.PageError as e:
                # await channel.send("Okay, ich habe das Folgende dazu auf Wikipedia gefunden: ")
                response = wikipedia.summary(wikipedia.suggest(query))
                await channel.send(response)
                return

            except discord.HTTPException as e:
                """
                print(query.split(' ',1)[1])
                await channel.send(wikipedia.summary(msg.split(' ',1)[1]))
                
                """
                await channel.send("Okay ich habe doch nichts auf Wikipedia gefunden. Irgendwas ist da schief gelaufen")
                return
        else:
            response = kernel.respond(message.content)
            await asyncio.sleep(random.randint(0, 2))
            await channel.send(response)

    # Finally, set the bot running
    client.run(settings.BOT_TOKEN)


###############################################################################


if __name__ == "__main__":
    main()
