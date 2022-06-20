import json
import logging
import random
from logging.handlers import RotatingFileHandler

import requests
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, filters, MessageHandler

import constants

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


async def unknown(update: Update, context: CallbackContext):
	await context.bot.send_message(chat_id=update.effective_chat.id, text=constants.UNKNOWN)


async def random_bestemmia(update: Update, context: CallbackContext):
	context.args.append(random.choice(constants.MOSCONI_ARRAY))
	response = requests.get(constants.RANDOM_BESTEMMIA_URL)
	json_object = json.loads(response.text)
	bestemmia = json_object["bestemmia"]
	await context.bot.send_message(chat_id=update.effective_chat.id, text=bestemmia)
	await tts(update, context, constants.IT, bestemmia)
	await play_taunt(update, context)


async def random_meme(update: Update, context: CallbackContext):
	response = requests.get(constants.RANDOM_MEME_URL)
	json_object = json.loads(response.text)
	await context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=json_object["url"])


async def random_gif(update: Update, context: CallbackContext):
	response = requests.get(constants.RANDOM_GIF_URL)
	json_object = json.loads(response.text)
	mp4 = json_object["data"]["images"]["original_mp4"]["mp4"]
	await context.bot.sendDocument(chat_id=update.effective_chat.id, document=mp4)


async def random_daoc(update: Update, context: CallbackContext):
	audio = constants.SIMONECELIA_DATA_URL + random.choice(constants.DAOC_ARRAY) + constants.MP3
	await context.bot.sendAudio(chat_id=update.effective_chat.id, audio=audio)


async def random_ts(update: Update, context: CallbackContext):
	audio = constants.SIMONECELIA_DATA_URL + random.choice(constants.TS_ARRAY) + constants.MP3
	await context.bot.sendAudio(chat_id=update.effective_chat.id, audio=audio)


async def random_aoe(update: Update, context: CallbackContext):
	audio = constants.SIMONECELIA_DATA_URL + random.choice(constants.AOE_ARRAY) + constants.MP3
	await context.bot.sendAudio(chat_id=update.effective_chat.id, audio=audio)


async def play_taunt(update: Update, context: CallbackContext):
	taunt = ' '.join(context.args).strip()
	if "" == taunt:
		await context.bot.send_message(chat_id=update.effective_chat.id, text=constants.ERROR_PARAMETER_NEEDED)
	else:
		if taunt in constants.DAOC_ARRAY or taunt in constants.TS_ARRAY or taunt in constants.AOE_ARRAY:
			audio = constants.SIMONECELIA_DATA_URL + taunt + constants.MP3
			await context.bot.sendAudio(chat_id=update.effective_chat.id, audio=audio)
		else:
			await context.bot.send_message(chat_id=update.effective_chat.id, text=constants.TAUNT_NOT_FOUND)
			logging.error("Taunt not found, input text = " + taunt)


async def list_taunts(update: Update, context: CallbackContext):
	await context.bot.send_message(chat_id=update.effective_chat.id, text=constants.TS_BOT_WEB_LINK)


async def tts_en(update: Update, context: CallbackContext):
	await tts(update, context, constants.EN, ' '.join(context.args))


async def tts_it(update: Update, context: CallbackContext):
	await tts(update, context, constants.IT, ' '.join(context.args))


async def tts_es(update: Update, context: CallbackContext):
	await tts(update, context, constants.ES, ' '.join(context.args))


async def tts(update: Update, context: CallbackContext, language, text):
	text = text.strip()
	if "" == text:
		await context.bot.send_message(chat_id=update.effective_chat.id, text=constants.ERROR_PARAMETER_NEEDED)
	else:
		myobj = gTTS(text=text, lang=language, slow=False)
		myobj.save(constants.MP3_TEMP_FILE)
		await context.bot.sendAudio(chat_id=update.effective_chat.id, audio=open(constants.MP3_TEMP_FILE, "rb"))


def get_version():
	with open("changelog.txt") as f:
		firstline = f.readline().rstrip()
	logging.info("Starting FoldoBot, " + firstline)


if __name__ == '__main__':
	application = ApplicationBuilder().token(constants.TOKEN).build()
	application.add_handler(CommandHandler('random_bestemmia', random_bestemmia))
	application.add_handler(CommandHandler('random_meme', random_meme))
	application.add_handler(CommandHandler('random_gif', random_gif))
	application.add_handler(CommandHandler('random_daoc', random_daoc))
	application.add_handler(CommandHandler('random_ts', random_ts))
	application.add_handler(CommandHandler('random_aoe', random_aoe))
	application.add_handler(CommandHandler('play_taunt', play_taunt))
	application.add_handler(CommandHandler('list_taunts', list_taunts))
	application.add_handler(CommandHandler('tts_en', tts_en))
	application.add_handler(CommandHandler('tts_es', tts_es))
	application.add_handler(CommandHandler('tts_it', tts_it))
	application.add_handler(MessageHandler(filters.COMMAND, unknown))
	get_version()
	application.run_polling(stop_signals=None)
