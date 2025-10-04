from aiogram import Bot, Dispatcher
from app.config import TOKEN

from app.hendlers.hendlers import rt
from app.hendlers.reg_admin_hendlers import admin_rt
from app.hendlers.reg_user_hendlers import user_rt
from database.db import async_main


import asyncio
import logging




async def main():
    await async_main()

    bot = Bot(TOKEN)
    dp = Dispatcher()

    
    dp.include_router(user_rt)
    dp.include_router(rt)
    dp.include_router(admin_rt)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(exit)