import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from routers.start import router as router_start
from routers.random_anec_from_categories import router as router_random_anec_from_cat
from routers.random_anec import router as router_random_anec
from routers.random_anecs import router as router_random_anecs
from routers.add_anec import router as router_add_anec
from routers.message import router as router_message
from routers.info import router as info

from config import bot_token


# Создаем бота и диспетчер
dp = Dispatcher()
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Запуск бота
async def main() -> None:
    dp.include_router(router_start)
    dp.include_router(router_random_anec_from_cat)
    dp.include_router(router_random_anec)
    dp.include_router(router_random_anecs)
    dp.include_router(router_add_anec)
    dp.include_router(router_message)
    dp.include_router(info)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())