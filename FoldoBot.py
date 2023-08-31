import html
import json
import logging as log
import os
import random
import signal
import sys
import time as time_os
import traceback
import warnings
from datetime import time
from logging.handlers import RotatingFileHandler

import pytz
import requests
from gtts import gTTS
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, ContextTypes, Application, AIORateLimiter
from telegram.request import HTTPXRequest

import constants as c
from BotApp import BotApp

log.basicConfig(
	handlers=[
		RotatingFileHandler(
			'_FoldoBot.log',
			maxBytes=10240000,
			backupCount=5
		),
		log.StreamHandler()
	],
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=c.LOG_LEVEL
)


async def send_dipre(update: Update, context: CallbackContext):
	log_bot_event(update, 'dipre')
	await context.bot.send_video(chat_id=update.effective_chat.id, video="assets/dipre.mp4")


async def send_zelensky(update: Update, context: CallbackContext):
	log_bot_event(update, 'zelensky')
	await context.bot.send_video(chat_id=update.effective_chat.id, video="assets/zelensky.mp4")


async def send_todobien(update: Update, context: CallbackContext):
	log_bot_event(update, 'todobien')
	await context.bot.send_video(chat_id=update.effective_chat.id, video="assets/todobien.mp4")


async def send_sivola130(update: Update, context: CallbackContext):
	log_bot_event(update, "sivola130")
	await context.bot.send_video(chat_id=update.effective_chat.id, video="assets/sivola130.mp4")


async def random_bestemmia(update: Update, context: CallbackContext):
	log_bot_event(update, 'random_bestemmia')
	context.args.append(random.choice(c.MOSCONI_ARRAY))
	try:
		response = requests.get(c.RANDOM_BESTEMMIA_URL)
		json_object = json.loads(response.text)
		bestemmia = json_object["bestemmia"]
		await context.bot.send_message(chat_id=update.effective_chat.id, text=bestemmia)
		await tts(update, context, bestemmia.lower())
		await play(update, context)
	except Exception as ex:
		log.error(ex)
		await context.bot.send_message(chat_id=update.effective_chat.id, text=c.ERROR_BESTEMMIA_MESSAGE)


async def random_meme(update: Update, context: CallbackContext):
	log_bot_event(update, 'random_meme')
	try:
		response = requests.get(c.RANDOM_MEME_URL)
		json_object = json.loads(response.text)
		await context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=json_object["url"])
	except Exception as ex:
		log.error(ex)
		await context.bot.send_message(chat_id=update.effective_chat.id, text=c.ERROR_MEME_MESSAGE)


async def random_gif(update: Update, context: CallbackContext):
	log_bot_event(update, 'random_gif')
	try:
		response = requests.get(c.RANDOM_GIF_URL)
		json_object = json.loads(response.text)
		mp4 = json_object["data"]["images"]["original_mp4"]["mp4"]
		await context.bot.sendDocument(chat_id=update.effective_chat.id, document=mp4)
	except Exception as ex:
		log.error(ex)
		await context.bot.send_message(chat_id=update.effective_chat.id, text=c.ERROR_GIF_MESSAGE)


async def random_taunt(update: Update, context: CallbackContext):
	log_bot_event(update, 'random_taunt')
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
	log_bot_event(update, 'play')
	taunt = c.SPACE.join(context.args).strip()
	if c.EMPTY == taunt:
		await context.bot.send_message(chat_id=update.effective_chat.id, text=c.ERROR_PARAMETER_NEEDED_MESSAGE)
	else:
		if taunt in c.DAOC_ARRAY or taunt in c.TS_ARRAY or taunt in c.AOE_ARRAY or taunt in c.DIPRE_ARRAY:
			audio = c.TS_BOT_WEB_DATA_URL + taunt + c.MP3
			await context.bot.send_audio(chat_id=update.effective_chat.id, audio=audio)
		else:
			await context.bot.send_message(chat_id=update.effective_chat.id, text=c.ERROR_TAUNT_NOT_FOUND_MESSAGE)
			log.error(f"Taunt not found, input text = {taunt}")


async def list_play(update: Update, context: CallbackContext):
	log_bot_event(update, 'list_play')
	await context.bot.send_message(chat_id=update.effective_chat.id, text=c.TS_BOT_WEB_URL)


async def tts(update: Update, context: CallbackContext, text=''):
	log_bot_event(update, 'tts')
	language = c.IT
	if c.EMPTY == text:
		cmd = update.message.text
		if cmd.startswith(c.SLASH + c.TTS_ES):
			language = c.ES
		elif cmd.startswith(c.SLASH + c.TTS_EN):
			language = c.EN
		text = c.SPACE.join(context.args).strip()
	if c.EMPTY == text:
		await context.bot.send_message(chat_id=update.effective_chat.id, text=c.ERROR_PARAMETER_NEEDED_MESSAGE)
	else:
		myobj = gTTS(text=text, lang=language, slow=False)
		myobj.save(c.MP3_TEMP_FILE)
		await context.bot.send_audio(chat_id=update.effective_chat.id, audio=c.MP3_TEMP_FILE)


async def send_amazon(update: Update, context: CallbackContext):
	log_bot_event(update, 'send_amazon')
	await context.bot.send_message(chat_id=update.effective_chat.id, text=c.AMAZON_MESSAGE)


async def send_version(update: Update, context: CallbackContext):
	log_bot_event(update, 'send_version')
	await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{get_version()} {c.VERSION_MESSAGE}')


async def send_shutdown(update: Update, context: CallbackContext):
	log_bot_event(update, 'send_shutdown')
	if update.effective_user.id == int(c.TELEGRAM_DEVELOPER_CHAT_ID):
		os.kill(os.getpid(), signal.SIGINT)
	else:
		await context.bot.send_message(chat_id=update.effective_chat.id, text=c.ERROR_NO_GRANT_SHUTDOWN)


async def dai_che_e_venerdi(context: CallbackContext):
	await context.bot.send_audio(chat_id=c.TELEGRAM_GROUP_ID, audio="assets/venerdi.mp3")


async def post_init(app: Application):
	version = get_version()
	log.info(f"Starting FoldoBot, {version}")
	if c.SEND_START_AND_STOP_MESSAGE == c.TRUE:
		await app.bot.send_message(chat_id=c.TELEGRAM_GROUP_ID, text=c.STARTUP_MESSAGE + version, parse_mode=ParseMode.HTML)
		await app.bot.send_message(chat_id=c.TELEGRAM_DEVELOPER_CHAT_ID, text=c.STARTUP_MESSAGE + version, parse_mode=ParseMode.HTML)


async def post_shutdown(app: Application):
	log.info(f"Shutting down, bot id={str(app.bot.id)}")


# v1.0, highest
def log_bot_event(update: Update, method_name: str):
	msg = '>>No message<<'
	if update.message is not None:
		msg = update.message.text
	user = update.effective_user.first_name
	uid = update.effective_user.id
	log.info(f"[method={method_name}] Got this message from {user} [id={str(uid)}]: {msg}")


# Log the error and send a telegram message to notify the developer. Attemp to restart the bot too
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
	# Log the error before we do anything else, so we can see it even if something breaks.
	log.error(msg="Exception while handling an update:", exc_info=context.error)
	# traceback.format_exception returns the usual python message about an exception, but as a
	# list of strings rather than a single string, so we have to join them together.
	tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
	tb_string = "".join(tb_list)
	# Build the message with some markup and additional information about what happened.
	update_str = update.to_dict() if isinstance(update, Update) else str(update)
	await context.bot.send_message(chat_id=c.TELEGRAM_DEVELOPER_CHAT_ID, text=f"An exception was raised while handling an update")
	await send_error_message(context, f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>")
	await send_error_message(context, f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>")
	await send_error_message(context, f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>")
	await send_error_message(context, f"<pre>{html.escape(tb_string)}</pre>")
	# Restart the bot
	time_os.sleep(5.0)
	os.execl(sys.executable, sys.executable, *sys.argv)


async def send_error_message(context: ContextTypes.DEFAULT_TYPE, message):
	max_length = 4096  # Maximum allowed length for a message
	chunks = [message[i:i + max_length] for i in range(0, len(message), max_length)]
	# Send each chunk as a separate message
	for chunk in chunks:
		if not chunk.startswith('<pre>'):
			chunk = '<pre>' + chunk
		if not chunk.endswith('</pre>'):
			chunk += '</pre>'
		# Finally, send the message
		await context.bot.send_message(chat_id=c.TELEGRAM_DEVELOPER_CHAT_ID, text=chunk, parse_mode=ParseMode.HTML)


def get_version():
	with open("changelog.txt") as f:
		firstline = f.readline().rstrip()
	return firstline


if __name__ == '__main__':
	application = ApplicationBuilder() \
		.token(c.TOKEN) \
		.application_class(BotApp) \
		.post_init(post_init) \
		.post_shutdown(post_shutdown) \
		.rate_limiter(AIORateLimiter(max_retries=c.AIO_RATE_LIMITER_MAX_RETRIES)) \
		.request(HTTPXRequest(http_version=c.HTTP_VERSION)) \
		.get_updates_request(HTTPXRequest(http_version=c.HTTP_VERSION)) \
		.build()
	application.add_handler(CommandHandler(c.DIPRE_MAJOR, send_dipre))
	application.add_handler(CommandHandler(c.RANDOM_BESTEMMIA, random_bestemmia))
	application.add_handler(CommandHandler(c.RANDOM_MEME, random_meme))
	application.add_handler(CommandHandler(c.RANDOM_GIF, random_gif))
	application.add_handler(CommandHandler([c.RANDOM_DAOC, c.RANDOM_TS, c.RANDOM_AOE, c.RANDOM_DIPRE], random_taunt))
	application.add_handler(CommandHandler('play', play))
	application.add_handler(CommandHandler('list_play', list_play))
	application.add_handler(CommandHandler([c.TTS_EN, c.TTS_ES, c.TTS_IT], tts))
	application.add_handler(CommandHandler('amazon', send_amazon))
	application.add_handler(CommandHandler('version', send_version))
	application.add_handler(CommandHandler('shutdown', send_shutdown))
	application.add_handler(CommandHandler('zelensky', send_zelensky))
	application.add_handler(CommandHandler('todobien', send_todobien))
	application.add_handler(CommandHandler('sivola130', send_sivola130))
	if c.IGNORE_WARNINGS == c.TRUE:
		warnings.filterwarnings("ignore")
	# noinspection PyTypeChecker
	application.job_queue.run_daily(dai_che_e_venerdi, time=time(tzinfo=pytz.timezone('CET'), hour=6), days=[5])
	application.add_error_handler(error_handler)
	application.run_polling(allowed_updates=Update.ALL_TYPES)
