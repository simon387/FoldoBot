# FoldoBot

Personal Telegram Spam Bot

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
+ per info sul bot (group id,
  ecc): https://api.telegram.org/botXXX/getUpdates
+ https://github.com/python-telegram-bot/python-telegram-bot/wiki/

## Setup dev

+ ```pip install python-telegram-bot --upgrade```
+ ```pip install python-telegram-bot -U --pre```
+ Telegram web Z is better, dunno why

## Setup BotFather

1. ```/setcommands```
2. ```@FoldoBot```
3. copy paste this:

```
random_bestemmia - bestemmia random
random_meme - meme random
random_gif - random gif
random_daoc - random daoc sound
random_ts - random teamspeak audio
random_aoe - random Age Of Empires sound
random_dipre - random dipre trash audio
play - plays specific taunt; e.g.: play r1
list_play - list all taunts of the bot
tts_en - play tts in english; e.g: tts_en hi
tts_it - play tts in italian; e.g: tts_it ciao
tts_es - play tts in spanish; e.g: tts_es hola
```

## Config file format

```
[secrets]
telegram.token=XXX
api.giphy.com.key=YYY

```