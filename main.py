import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from database import async_db_manager
from handlers.common import common_router
from handlers.menu import menu


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=config.TG_API_KEY.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(common_router, menu)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
