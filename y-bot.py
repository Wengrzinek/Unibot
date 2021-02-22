# from template
import sys

import settings
import discord
import message_handler

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from events.base_event              import BaseEvent
from events                         import *
from multiprocessing                import Process

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
    model = ""

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

    #from https://towardsdatascience.com/how-to-build-your-own-ai-chatbot-on-discord-c6b3468189f4
    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        else:
            inp = message.content
            #result = model.predict([bag_of_words(inp, words)])[0]
            #result_index = np.argmax(result)
            #tag = labels[result_index]

            #if result[result_index] > 0.7:
             #   for tg in data["intents"]:
               #     if tg['tag'] == tag:
                #        responses = tg['responses']

                #bot_response = random.choice(responses)
                #await message.channel.send(bot_response.format(message))
           # else:
              #  await message.channel.send("Entschuldigung ich habe das nicht verstanden.".format(message))

    @client.event
    async def on_message(message):
        await common_handle_message(message)

    @client.event
    async def on_message_edit(before, after):
        await common_handle_message(after)

    # Finally, set the bot running
    client.run(settings.BOT_TOKEN)

###############################################################################


if __name__ == "__main__":
    main()
