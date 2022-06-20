#
# script di demo
#
# import exchange
import logging

from telegram.ext import CommandHandler, Updater

# import requests

TOKEN = "XXX"
CHAT_ID = "-1001659630309"
API_TELEGRAM = 'https://api.telegram.org/bot'
PARSE_MODE = '&parse_mode=HTML&disable_web_page_preview=false'


def send_telegram(text):
	logging.info('Sending info to telegram channel for')


#	requests.post(API_TELEGRAM + TOKEN + '/sendMessage?chat_id=' + CHAT_ID + '&text=' + text + PARSE_MODE)

def convert_usd(asd):
	logging.info("kek")


if __name__ == "__main__":
	log_format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%SECRETS")
	#
	# send_telegram("porco dio")
	upd = Updater(TOKEN, use_context=True)
	disp = upd.dispatcher

	disp.add_handler(CommandHandler("usd", convert_usd))
	# disp.add_handler(CommandHandler("eur", convert_eur))

	upd.start_polling()

	upd.idle()
