"""
unibot.py

The main bot file.
It used to be called y-bot, since we were still working with program-y in the past

"""

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
from discord.ext.commands import Bot

# Set to remember if the bot is already running, since on_ready may be called
# more than once on reconnects
this = sys.modules[__name__]
this.running = False

# Scheduler that will be used to manage events
sched = AsyncIOScheduler()

def main():
    # Initialize the client
    print("Starting up...")
    client = discord.Client()

    # AIML startup and "learning" process.
    unibot = aiml.Kernel()
    unibot.learn("learn-startup.xml")
    unibot.respond("LOAD AIML")

    # Wikipedia init - Set language to German
    wikipedia.set_lang("de")

    # Define event handlers for the client
    # on_ready may be called multiple times in the event of a reconnect,
    # hence the running flag

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

        # Load all events. Not really necessary but we can keep it.
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

    # code inspiration taken from https://towardsdatascience.com/how-to-build-your-own-ai-chatbot-on-discord-c6b3468189f4
    # and https://github.com/Assassinumz/Animus/ and of course the official Discord.py git repo
    @client.event
    async def on_message(message):
        channel = message.channel
        if message.author.bot or str(message.channel) != settings.CHANNEL_NAME:
            return

        if message.author == client.user:
            return

        if message.content is None:
            return

        if unibot.respond(message.content) == "s":
            return

        # Y_QUERY is the silent indicator for a wiki request. AIML throws out Y_QUERY followed by the search query.
        # Y_QUERY is used because it won't be likely used in natural language. If we would have been able to use
        # SPARQL, we could just exchange the wikipedia.py parts with SPARQL parts.
        if "Y_QUERY" in unibot.respond(message.content):
            msg = message.content
            # Cuts out the Y_QUERY and takes the rest
            query = msg[8:]
            try:
                await channel.send("Okay, ich habe das Folgende dazu auf Wikipedia gefunden: ")
                response = wikipedia.summary(query)
                await channel.send(response)
                return
            # Disambiguation errors occur if wikipedia.py finds more than one result for a given query.
            # We are just going to take the first result, although wikipedia is very much non-transparent
            # about how they sort results. We could also just use a random result at this point.
            except wikipedia.DisambiguationError as e:
                await channel.send(wikipedia.summary(e.options[0]))
                return
            # It could be that the user has just misspelled the query. Wikipedia.py offers a "suggest" function for
            # that. The suggest function is not very reliable though.
            except wikipedia.PageError as e:
                response = wikipedia.summary(wikipedia.suggest(query))
                await channel.send(response)
                return
            # If all fails, wikipedia.py will create issues causing Discord.py to throw an HTTP Exception. This will
            # generally happen whenever wikipedia can't find any results for the query.
            except discord.HTTPException as e:
                await channel.send("Okay ich habe doch nichts auf Wikipedia gefunden. Irgendwas ist da schief gelaufen")
                return
        # Regular message handling
        else:
            response = unibot.respond(message.content)
            await asyncio.sleep(random.randint(0, 2))
            await channel.send(response)

    # Finally, set the bot running
    client.run(settings.BOT_TOKEN)



if __name__ == "__main__":
    main()
