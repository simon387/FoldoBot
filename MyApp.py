from telegram.constants import ParseMode
from telegram.ext import Application
import constants as c


class MyApp(Application):
	async def stop(self):
		await super().stop()
		await self.bot.send_message(chat_id=c.TELEGRAM_GROUP_ID, text=c.SHUTDOWN_MESSAGE, parse_mode=ParseMode.HTML)
