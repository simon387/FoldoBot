import json
import logging
import random
from logging.handlers import RotatingFileHandler

import requests
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, filters, MessageHandler

import constants as cn

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
	await context.bot.send_message(chat_id=update.effective_chat.id, text=cn.UNKNOWN_COMMAND_RESPONSE)


async def random_bestemmia(update: Update, context: CallbackContext):
	context.args.append(random.choice(cn.MOSCONI_ARRAY))
	response = requests.get(cn.RANDOM_BESTEMMIA_URL)
	json_object = json.loads(response.text)
	bestemmia = json_object["bestemmia"]
	await context.bot.send_message(chat_id=update.effective_chat.id, text=bestemmia)
	await tts(update, context, bestemmia)
	await play(update, context)


async def random_meme(update: Update, context: CallbackContext):
	response = requests.get(cn.RANDOM_MEME_URL)
	json_object = json.loads(response.text)
	await context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=json_object["url"])


async def random_gif(update: Update, context: CallbackContext):
	response = requests.get(cn.RANDOM_GIF_URL)
	json_object = json.loads(response.text)
	mp4 = json_object["data"]["images"]["original_mp4"]["mp4"]
	await context.bot.sendDocument(chat_id=update.effective_chat.id, document=mp4)


async def random_taunt(update: Update, context: CallbackContext):
	taunt_array = cn.DAOC_ARRAY
	text = update.message.text
	if text.startswith(cn.SLASH + cn.RANDOM_TS):
		taunt_array = cn.TS_ARRAY
	elif text.startswith(cn.SLASH + cn.RANDOM_AOE):
		taunt_array = cn.AOE_ARRAY
	elif text.startswith(cn.SLASH + cn.RANDOM_DIPRE):
		taunt_array = cn.DIPRE_ARRAY
	audio = cn.SIMONECELIA_DATA_URL + random.choice(taunt_array) + cn.MP3
	await context.bot.sendAudio(chat_id=update.effective_chat.id, audio=audio)


async def play(update: Update, context: CallbackContext):
	taunt = ' '.join(context.args).strip()
	if '' == taunt:
		await context.bot.send_message(chat_id=update.effective_chat.id, text=cn.ERROR_PARAMETER_NEEDED)
	else:
		if taunt in cn.DAOC_ARRAY or taunt in cn.TS_ARRAY or taunt in cn.AOE_ARRAY or taunt in cn.DIPRE_ARRAY:
			audio = cn.SIMONECELIA_DATA_URL + taunt + cn.MP3
			await context.bot.sendAudio(chat_id=update.effective_chat.id, audio=audio)
		else:
			await context.bot.send_message(chat_id=update.effective_chat.id, text=cn.TAUNT_NOT_FOUND)
			logging.error("Taunt not found, input text = " + taunt)


async def list_play(update: Update, context: CallbackContext):
	await context.bot.send_message(chat_id=update.effective_chat.id, text=cn.TS_BOT_WEB_LINK)


async def tts(update: Update, context: CallbackContext, bestemmia=''):
	language = cn.IT
	if '' != bestemmia:
		text = bestemmia
	else:
		cmd = update.message.text
		if cmd.startswith(cn.SLASH + cn.TTS_ES):
			language = cn.ES
		elif cmd.startswith(cn.SLASH + cn.TTS_EN):
			language = cn.EN
		text = ' '.join(context.args).strip()
	if '' == text:
		await context.bot.send_message(chat_id=update.effective_chat.id, text=cn.ERROR_PARAMETER_NEEDED)
	else:
		myobj = gTTS(text=text, lang=language, slow=False)
		myobj.save(cn.MP3_TEMP_FILE)
		await context.bot.sendAudio(chat_id=update.effective_chat.id, audio=open(cn.MP3_TEMP_FILE, "rb"))


def get_version():
	with open("changelog.txt") as f:
		firstline = f.readline().rstrip()
	logging.info("Starting FoldoBot, " + firstline)


if __name__ == '__main__':
	application = ApplicationBuilder().token(cn.TOKEN).build()
	application.add_handler(CommandHandler('random_bestemmia', random_bestemmia))
	application.add_handler(CommandHandler('random_meme', random_meme))
	application.add_handler(CommandHandler('random_gif', random_gif))
	application.add_handler(CommandHandler(['random_daoc', cn.RANDOM_TS, cn.RANDOM_AOE, cn.RANDOM_DIPRE], random_taunt))
	application.add_handler(CommandHandler('play', play))
	application.add_handler(CommandHandler('list_play', list_play))
	application.add_handler(CommandHandler([cn.TTS_EN, cn.TTS_ES, cn.TTS_IT], tts))
	application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
	get_version()
	application.run_polling(stop_signals=None)
