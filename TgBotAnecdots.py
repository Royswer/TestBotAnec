import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import bot_token
from db_manager import DB

from bot import start
from bot.start import router as router_start
from bot import random_anec_from_categories
from bot.random_anec_from_categories import router as router_random_anec_from_cat
from bot import random_anec
from bot.random_anec import router as router_random_anec
from bot import random_anec_from_categories
from bot.random_anec import router as router_random_anecs
from bot import add_anec
from bot.add_anec import router as router_add_anec

# Создаем бота и диспетчер
dp = Dispatcher()
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

db_manager = DB('test.db')

# # Эхо для всех остальных сообщений
# @dp.message()
# async def echo_handler(message: Message):
#     await message.answer(f'Я тоже так могу: {message.text}')

# Запуск бота
async def main() -> None:
    dp.include_router(router_start)
    dp.include_router(router_random_anec_from_cat)
    dp.include_router(router_random_anec)
    dp.include_router(router_random_anecs)
    dp.include_router(router_add_anec)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())