import asyncio
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import random
from config import bot_token
from db_manager import DB


#Create
dp = Dispatcher()
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

db_manager = DB('test.db')

class DialogStates(StatesGroup):
    waiting_answer = State()

@dp.callback_query()
async def callback_query(callback: CallbackQuery):
    if callback.data == 'random_anec':
        await callback.message.answer(db_manager.get_random_anecdot())
    if callback.data == '3_anec':
        await callback.message.answer(db_manager.get_random_anecdots(3))
    if callback.data == 'add_anec':
        await callback.message.answer(text = "пока не придумал")
    if callback.data == 'select_cat':
        await callback.message.answer(text = "пока не придумал")
    await callback.answer()

#@dp.message(DialogStates.waiting_answer)
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer('Хорошо')
    await state.clear()

#Start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = 'Случайный анекдот', callback_data='random_anec')],
        [InlineKeyboardButton(text = '3 анекдота',callback_data='3_anec')],
        [InlineKeyboardButton(text = 'Добавить анекдот',callback_data='add_anec')],
        [InlineKeyboardButton(text = 'Выбрать категорию',callback_data='select_cat')],
        ])
    await message.answer(f"Привет! @{message.from_user.username}", reply_markup=markup)


#Эхо(дубль сообщения пользователя)
@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.answer(f'Я тоже так могу: {message.text}')
    except TypeError:
        await message.answer("Nice try!")

async def main() -> None:
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())