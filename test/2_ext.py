import logging

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, filters, InlineQueryHandler, \
	MessageHandler

logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=logging.INFO
)

TOKEN = "XXX"


# /start command
async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
	await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


# echo mode
async def echo(update: Update, context: CallbackContext.DEFAULT_TYPE):
	await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# caps command
async def caps(update: Update, context: CallbackContext):
	text_caps = ' '.join(context.args).upper()
	await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def inline_caps(update: Update, context: CallbackContext.DEFAULT_TYPE):
	query = update.inline_query.query
	if not query:
		return
	results = []
	results.append(
		InlineQueryResultArticle(
			id=query.upper(),
			title='Caps',
			input_message_content=InputTextMessageContent(query.upper())
		)
	)
	await context.bot.answer_inline_query(update.inline_query.id, results)


async def unknown(update: Update, context: CallbackContext.DEFAULT_TYPE):
	await context.bot.send_message(chat_id=update.effective_chat.id, text="Scusa? Cazzo dici?")


if __name__ == '__main__':
	application = ApplicationBuilder().token(TOKEN).build()

	start_handler = CommandHandler('start', start)
	application.add_handler(start_handler)

	# echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
	# application.add_handler(echo_handler)

	caps_handler = CommandHandler('caps', caps)
	application.add_handler(caps_handler)

	inline_caps_handler = InlineQueryHandler(inline_caps)
	application.add_handler(inline_caps_handler)

	# Other handlers
	unknown_handler = MessageHandler(filters.COMMAND, unknown)
	application.add_handler(unknown_handler)

	application.run_polling()
