from aiogram import Router, F
from aiogram.types import Message


router = Router()

# Эхо для всех остальных сообщений
@router.message()
async def echo_handler(message: Message):
    await message.answer(f'Я тоже так могу: {message.text}')
    print(message)