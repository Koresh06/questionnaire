import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, find_dotenv

from app.database.models import async_main
from app.handlers.users.user import router
from app.handlers.admin.admin import admin

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info('Staring bot')
    
    await async_main() #Запуск БД
    bot: Bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')
    dp: Dispatcher = Dispatcher()
    
    dp.include_routers(
        admin,
        router
    )
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as exx:
        print(exit())