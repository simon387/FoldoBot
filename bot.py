import json
import logging
import random
from logging.handlers import RotatingFileHandler

import requests
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, filters, MessageHandler

import constants as cons

logging.basicConfig(
	handlers=[
		RotatingFileHandler(
			'FoldoBot.log',
			maxBytes=10240000,
			backupCount=5
		),
		logging.StreamHandler()
	],
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.DEBUG
)


async def unknown_command(update: Update, context: CallbackContext):
	await context.bot.send_message(chat_id=update.effective_chat.id, text=cons.UNKNOWN_COMMAND_RESPONSE)


async def random_bestemmia(update: Update, context: CallbackContext):
	context.args.append(random.choice(cons.MOSCONI_ARRAY))
	response = requests.get(cons.RANDOM_BESTEMMIA_URL)
	json_object = json.loads(response.text)
	bestemmia = json_object["bestemmia"]
	await context.bot.send_message(chat_id=update.effective_chat.id, text=bestemmia)
	await tts(update, context, bestemmia)
	await play(update, context)


async def random_meme(update: Update, context: CallbackContext):
	response = requests.get(cons.RANDOM_MEME_URL)
	json_object = json.loads(response.text)
	await context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=json_object["url"])


async def random_gif(update: Update, context: CallbackContext):
	response = requests.get(cons.RANDOM_GIF_URL)
	json_object = json.loads(response.text)
	mp4 = json_object["data"]["images"]["original_mp4"]["mp4"]
	await context.bot.sendDocument(chat_id=update.effective_chat.id, document=mp4)


async def random_taunt(update: Update, context: CallbackContext):
	taunt_array = cons.DAOC_ARRAY
	text = update.message.text
	if text.startswith('/random_ts'):
		taunt_array = cons.TS_ARRAY
	elif text.startswith('/random_aoe'):
		taunt_array = cons.AOE_ARRAY
	elif text.startswith('/random_dipre'):
		taunt_array = cons.DIPRE_ARRAY
	audio = cons.SIMONECELIA_DATA_URL + random.choice(taunt_array) + cons.MP3
	await context.bot.sendAudio(chat_id=update.effective_chat.id, audio=audio)


async def play(update: Update, context: CallbackContext):
	taunt = ' '.join(context.args).strip()
	if '' == taunt:
		await context.bot.send_message(chat_id=update.effective_chat.id, text=cons.ERROR_PARAMETER_NEEDED)
	else:
		if taunt in cons.DAOC_ARRAY or taunt in cons.TS_ARRAY or taunt in cons.AOE_ARRAY or taunt in cons.DIPRE_ARRAY:
			audio = cons.SIMONECELIA_DATA_URL + taunt + cons.MP3
			await context.bot.sendAudio(chat_id=update.effective_chat.id, audio=audio)
		else:
			await context.bot.send_message(chat_id=update.effective_chat.id, text=cons.TAUNT_NOT_FOUND)
			logging.error("Taunt not found, input text = " + taunt)


async def list_play(update: Update, context: CallbackContext):
	await context.bot.send_message(chat_id=update.effective_chat.id, text=cons.TS_BOT_WEB_LINK)


async def tts(update: Update, context: CallbackContext, bestemmia=''):
	language = cons.IT
	if '' != bestemmia:
		text = bestemmia
	else:
		cmd = update.message.text
		if cmd.startswith('/tts_es'):
			language = cons.ES
		elif cmd.startswith('/tts_en'):
			language = cons.EN
		text = ' '.join(context.args).strip()
	if '' == text:
		await context.bot.send_message(chat_id=update.effective_chat.id, text=cons.ERROR_PARAMETER_NEEDED)
	else:
		myobj = gTTS(text=text, lang=language, slow=False)
		myobj.save(cons.MP3_TEMP_FILE)
		await context.bot.sendAudio(chat_id=update.effective_chat.id, audio=open(cons.MP3_TEMP_FILE, "rb"))


def get_version():
	with open("changelog.txt") as f:
		firstline = f.readline().rstrip()
	logging.info("Starting FoldoBot, " + firstline)


if __name__ == '__main__':
	application = ApplicationBuilder().token(cons.TOKEN).build()
	application.add_handler(CommandHandler('random_bestemmia', random_bestemmia))
	application.add_handler(CommandHandler('random_meme', random_meme))
	application.add_handler(CommandHandler('random_gif', random_gif))
	application.add_handler(CommandHandler(['random_daoc', 'random_ts', 'random_aoe', 'random_dipre'], random_taunt))
	application.add_handler(CommandHandler('play', play))
	application.add_handler(CommandHandler('list_play', list_play))
	application.add_handler(CommandHandler(['tts_en', 'tts_es', 'tts_it'], tts))
	application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
	get_version()
	application.run_polling(stop_signals=None)
