import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from app.user import user
from app.admin import admin

from config import TOKEN

from app.database.models import async_main


commands = [
    BotCommand(command="/start", description="Начать работу с ботом"),
    BotCommand(command="/history", description="Показать историю изображений")
]

async def set_bot_commands(bot: Bot):
    await bot.set_my_commands(commands)
async def main():
    bot = Bot(token=TOKEN,
              # default=DefaultBotProperties(parse_mode=ParseMode.HTML)
              )

    dp = Dispatcher()
    await set_bot_commands(bot)
    dp.include_routers(user, admin)
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)

    await dp.start_polling(bot)


async def startup(dispatcher: Dispatcher):
    await async_main()
    print('Starting up...')


async def shutdown(dispatcher: Dispatcher):
    print('Shutting down...')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
