# FoldoBot

Telegram Bot used for my Telegram friend's group; it spams fun things.

## BotFather

Done! Congratulations on your new bot. You will find it at t.me/FoldoBot. You can now add a description, about section
and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool
bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you
do this.

Use this token to access the HTTP API:
XXX
Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api

## Info

+ python --version 3.10.4
+ pip show python-telegram-bot 20.0a1
+ bot info (group id, ecc): https://api.telegram.org/botXXX/getUpdates
+ https://github.com/python-telegram-bot/python-telegram-bot/wiki/
+ pip install python-telegram-bot[rate-limiter]

## Setup dev

+ ```pip install python-telegram-bot --upgrade``` or ```pip install python-telegram-bot -U --pre```
+ ```pip install gtts```
+ web client: Telegram web Z is better, dunno why
+ ```pip install python-telegram-bot[rate-limiter]```

## Test / Production

Tested and deployed on https://www.pythonanywhere.com and it works!

## Setup BotFather

1. ```/setcommands```
2. ```@FoldoBot```
3. copy paste this:

```
bestemmia - bestemmia random
meme - meme random
gif - random gif
daoc - random daoc sound
ts - random teamspeak audio
aoe - random Age Of Empires sound
dipre - random dipre trash audio
play - plays specific taunt; e.g.: play r1
list_play - list all taunts of the bot
tts_en - play tts in english; e.g: tts_en hi
tts_it - play tts in italian; e.g: tts_it ciao
tts_es - play tts in spanish; e.g: tts_es hola
dipre_mayor - play dipre in a mayor situation
amazon - show amazon friendly channels
version - show bot's version
```

## Config file format

Name: ```config.properties```

```
[secrets]
telegram.token=XXX
api.giphy.com.key=YYY
telegram.group.id=-ZZZ
telegram.developer.chat.id=WWW
[application]
ignore.warnings=true
# log.level = info | debug | error
log.level=info
send.start.and.stop.message=false
```

## Random util commands

+ Run from detached ssh: ```nohup python bot.py &```
+ Show python processes: ```ps -ef | grep python```

## Usefull Links

+ https://github.com/D3vd/Meme_Api
+ https://www.pythonanywhere.com/whitelist/
+ https://support.anaconda.com/hc/en-us/requests/
+ https://docs.python-telegram-bot.org/
