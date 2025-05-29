import asyncio
from aiogram import Dispatcher
import logging

from bot.handlers.handlers import router
from config import bot

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger()

dp = Dispatcher()
dp.include_routers(router)

async def main():

    task = asyncio.create_task(dp.start_polling(bot))
    task.set_name("Bot")
    logger.info("Бот запущен")
    
    await task

if __name__ == '__main__':
    asyncio.run(main())
