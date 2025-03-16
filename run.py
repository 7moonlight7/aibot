import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv


from app.user import user
from app.admin import admin
from app.database.models import async_main


logging.basicConfig(level=logging.INFO)



async def main():
    load_dotenv()
    bot = Bot(os.getenv('TG_TOKEN'))
    dp = Dispatcher()
    dp.include_routers(user, admin)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    await async_main()
    print('Starting up...')


async def shutdown(dispatcher: Dispatcher):
    print('Shutting down...')

if __name__ == 'main':
    try:
        asyncio.run(main)
    except:
        print('EXIT')