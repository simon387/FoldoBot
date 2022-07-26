import html
import json
import logging
import os
import random
import sys
import time as time_os
from datetime import time
import traceback
from logging.handlers import RotatingFileHandler

import pytz
import requests
from gtts import gTTS
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, ContextTypes, filters, MessageHandler

import constants as c

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
	level=logging.INFO
)


async def dipre(update: Update, context: CallbackContext):
	await context.bot.send_video(chat_id=update.effective_chat.id, video=open("assets/dipre.mp4", c.RB))


async def random_bestemmia(update: Update, context: CallbackContext):
	context.args.append(random.choice(c.MOSCONI_ARRAY))
	response = requests.get(c.RANDOM_BESTEMMIA_URL)
	json_object = json.loads(response.text)
	bestemmia = json_object["bestemmia"]
	await context.bot.send_message(chat_id=update.effective_chat.id, text=bestemmia)
	await tts(update, context, bestemmia)
	await play(update, context)


async def random_meme(update: Update, context: CallbackContext):
	response = requests.get(c.RANDOM_MEME_URL)
	json_object = json.loads(response.text)
	await context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=json_object["url"])


async def random_gif(update: Update, context: CallbackContext):
	response = requests.get(c.RANDOM_GIF_URL)
	json_object = json.loads(response.text)
	mp4 = json_object["data"]["images"]["original_mp4"]["mp4"]
	await context.bot.sendDocument(chat_id=update.effective_chat.id, document=mp4)


async def random_taunt(update: Update, context: CallbackContext):
	taunt_array = c.DAOC_ARRAY
	text = update.message.text
	if text.startswith(c.SLASH + c.RANDOM_TS):
		taunt_array = c.TS_ARRAY
	elif text.startswith(c.SLASH + c.RANDOM_AOE):
		taunt_array = c.AOE_ARRAY
	elif text.startswith(c.SLASH + c.RANDOM_DIPRE):
		taunt_array = c.DIPRE_ARRAY
	audio = c.TS_BOT_WEB_DATA_URL + random.choice(taunt_array) + c.MP3
	await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio)


async def play(update: Update, context: CallbackContext):
	taunt = c.SPACE.join(context.args).strip()
	if c.EMPTY == taunt:
		await context.bot.send_message(chat_id=update.effective_chat.id, text=c.ERROR_PARAMETER_NEEDED)
	else:
		if taunt in c.DAOC_ARRAY or taunt in c.TS_ARRAY or taunt in c.AOE_ARRAY or taunt in c.DIPRE_ARRAY:
			audio = c.TS_BOT_WEB_DATA_URL + taunt + c.MP3
			await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio)
		else:
			await context.bot.send_message(chat_id=update.effective_chat.id, text=c.TAUNT_NOT_FOUND)
			logging.error("Taunt not found, input text = " + taunt)


async def list_play(update: Update, context: CallbackContext):
	await context.bot.send_message(chat_id=update.effective_chat.id, text=c.TS_BOT_WEB_LINK)


async def tts(update: Update, context: CallbackContext, text=''):
	language = c.IT
	if c.EMPTY == text:
		cmd = update.message.text
		if cmd.startswith(c.SLASH + c.TTS_ES):
			language = c.ES
		elif cmd.startswith(c.SLASH + c.TTS_EN):
			language = c.EN
		text = c.SPACE.join(context.args).strip()
	if c.EMPTY == text:
		await context.bot.send_message(chat_id=update.effective_chat.id, text=c.ERROR_PARAMETER_NEEDED)
	else:
		myobj = gTTS(text=text, lang=language, slow=False)
		myobj.save(c.MP3_TEMP_FILE)
		await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(c.MP3_TEMP_FILE, c.RB))


async def unknown_command(update: Update, context: CallbackContext):
	await context.bot.send_message(chat_id=update.effective_chat.id, text=c.UNKNOWN_COMMAND_RESPONSE)


async def amazon(update: Update, context: CallbackContext):
	await context.bot.send_message(chat_id=update.effective_chat.id, text=c.AMAZON_MESSAGE)


async def dai_che_e_venerdi(context: CallbackContext):
	await context.bot.send_audio(chat_id=c.TELEGRAM_GROUP_ID, audio=open("assets/venerdi.mp3", c.RB))


# Log the error and send a telegram message to notify the developer. Attemp to restart the bot too
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
	# Log the error before we do anything else, so we can see it even if something breaks.
	logging.error(msg="Exception while handling an update:", exc_info=context.error)
	# traceback.format_exception returns the usual python message about an exception, but as a
	# list of strings rather than a single string, so we have to join them together.
	tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
	tb_string = "".join(tb_list)
	# Build the message with some markup and additional information about what happened.
	# You might need to add some logic to deal with messages longer than the 4096 character limit.
	update_str = update.to_dict() if isinstance(update, Update) else str(update)
	message = (
		f"An exception was raised while handling an update\n"
		f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
		"</pre>\n\n"
		f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
		f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
		f"<pre>{html.escape(tb_string)}</pre>"
	)
	# Finally, send the message
	await context.bot.send_message(chat_id=c.TELEGRAM_DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)
	# Restart the bot
	time_os.sleep(5.0)
	os.execl(sys.executable, sys.executable, *sys.argv)


def get_version():
	with open("changelog.txt") as f:
		firstline = f.readline().rstrip()
	logging.info("Starting FoldoBot, " + firstline)


if __name__ == '__main__':
	application = ApplicationBuilder().token(c.TOKEN).build()
	application.add_handler(CommandHandler('dipre', dipre))
	application.add_handler(CommandHandler('random_bestemmia', random_bestemmia))
	application.add_handler(CommandHandler('random_meme', random_meme))
	application.add_handler(CommandHandler('random_gif', random_gif))
	application.add_handler(CommandHandler([c.RANDOM_DAOC, c.RANDOM_TS, c.RANDOM_AOE, c.RANDOM_DIPRE], random_taunt))
	application.add_handler(CommandHandler('play', play))
	application.add_handler(CommandHandler('list_play', list_play))
	application.add_handler(CommandHandler([c.TTS_EN, c.TTS_ES, c.TTS_IT], tts))
	application.add_handler(CommandHandler('amazon', amazon))
	application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
	application.job_queue.run_daily(dai_che_e_venerdi, time=time(tzinfo=pytz.timezone('CET')), days=[5])
	application.add_error_handler(error_handler)
	get_version()
	application.run_polling(stop_signals=None)
