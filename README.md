# Unibot
 
 This project was created for the THM class "Grundlagen der KI" in Semester 2020/2021. The idea of the project was to
 create a chatbot that is working on either IRC or Discord. We have opted for the Discord integration.
 
 Unibot is a German based AIML 1.0 chat bot that offers Discord server support as well as the ability to look up
 wikipedia articles.

# Installation 

Unibot itself will just run fine with a basic Python3 interpreter. Any requirements needed can be downloaded with the
requirements.txt file by calling `pip install -r requirements.txt` while in the project directory.

# Run

This project was built entirely around the concept of Discord integration. Running it without Discord appears to be an
unlikely endeavour.

To use Unibot yourself, you will need the Discord client and a Discord account.

When you have a Discord-Account, you will need to go to the 
[Discord Developer Portal](https://discord.com/developers/applications) and create a new application under any name.

![Discord New Application](https://imgur.com/CWQUhyD.png)

Select the new application and under Settings there should be an option called Bot.

![Bot](https://imgur.com/Puiex9L.png)
There you will find an `Add Bot`
button. The newly created bot has a Token field where you can regenerate or copy an existing bot token. Copy the existing
bot token and add it to `BOT_TOKEN` in `settings.py`. 

![BOT_TOKEN](https://imgur.com/tIC4Six.png)
Now you have created a link between unibot and Discord.

The next step is to create a Discord server. In the Discord client, press the plus button just above the
compass icon.

![New Server](https://imgur.com/GnkCJDy.png)

Follow the onscreen prompts to create a Discord server and name it whatever you want. You should now have your very 
own Discord server.

Back on the [Discord Developer Portal](https://discord.com/developers/applications), select your application.
Select the OAuth2 menu.

![OAuth2](https://imgur.com/bT6h2g3.png)

Here you will need to select the `bot` option in `Scopes`.

![Scopes](https://imgur.com/Fae7w4h.png)
Which should generate a bot invite link. Before you use the link on any web browser of your choice,
you will need to set the `Bot Permissions` to `Administrator`.

![Permissions](https://imgur.com/tWZg2pC.png)
Whilst you generally don't need all the permissions given by `Administrator`, it is the easiest way.

Now you can copy and use the bot invite link generated within ´Scopes´ with any modern web browser. There you should get
the option to Add the bot to any server you have created or have administrative rights over.

![Discord add bot](https://imgur.com/xikc49d.png)

If you have done everything correctly, you should now just be able to interact with Unibot in the #general chat of your
newly created server. By default, any text channel is enabled. If you want to limit the bot to a single text channel,
edit `CHANNEL_NAME` in `settings.py`






  
