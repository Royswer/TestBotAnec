import asyncio
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import bot_token
import random
import requests
from bs4 import BeautifulSoup


#Create
dp = Dispatcher()
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


#Start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет! @{message.from_user.username}")



#Эхо(дубль сообщения пользователя)
@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.answer('Я тоже так могу:')
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")

async def main() -> None:
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())