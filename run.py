import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_db_init


async def main():
    await async_db_init()
    load_dotenv()
    bot = Bot(token=os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filemode="a", filename="bot.log", encoding="UTF-8")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен!")
