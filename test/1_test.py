import asyncio

import telegram

TOKEN = "XXX"
CHAT_ID = "-1001659630309"


# info sul bot
# async def main():
# 	bot = telegram.Bot(TOKEN)
# 	async with bot:
# 		print(await bot.get_me())

# altre info
# async def main():
# 	bot = telegram.Bot(TOKEN)
# 	async with bot:
# 		print((await bot.get_updates())[0])

# send message
async def main():
	bot = telegram.Bot(TOKEN)
	async with bot:
		await bot.send_message(text='dio cane!', chat_id=CHAT_ID)


if __name__ == '__main__':
	asyncio.run(main())
