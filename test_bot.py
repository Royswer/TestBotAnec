import asyncio
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random
import requests
from bs4 import BeautifulSoup
from config import bot_token



#Create
dp = Dispatcher()
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

class DialogStates(StatesGroup):
    waiting_answer = State()

@dp.callback_query()
async def callback_query(callback: CallbackQuery):
    if callback.data == 'test1':
        await callback.message.answer(text = "привет")
    if callback.data == 'test2':
        await callback.message.answer(text = "пока не придумал")

@dp.message(Command('Test2'))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer('Как у тебя дела?')
    await state.set_state(DialogStates.waiting_answer)

@dp.message(DialogStates.waiting_answer)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer('Хорошо')
    await state.clear()

#Start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    markup = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text = 'Start'),KeyboardButton(text = 'Test2')],
        [KeyboardButton(text = 'Test3')],
        [KeyboardButton(text = 'Contact', request_contact=True)]
        ])
    await message.answer(f"Привет! @{message.from_user.username}", reply_markup=markup)

@dp.message(Command('Test'))
async def command_start_handler(message: Message) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = 'ТестируюКнопку',url='https://habr.com/ru/companies/otus/articles/769448/')
        ],
        [InlineKeyboardButton(text = 'ТестируюКнопку2',callback_data='test2')
        ]])
    await message.answer(f"Привет! @{message.from_user.username}", reply_markup=markup)



#Эхо(дубль сообщения пользователя)
@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.answer(f'Я тоже так могу: {message.text}')
        #await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")

async def main() -> None:
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())