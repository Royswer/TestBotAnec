from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton



router = Router()
# Главное меню
@router.message(CommandStart())
async def start_cmd(message: Message) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Случайный анекдот', callback_data='random_anec')],
        [InlineKeyboardButton(text='3 анекдота', callback_data='3_anec')],
        [InlineKeyboardButton(text='Добавить анекдот', callback_data='add_anec')],
        [InlineKeyboardButton(text='Выбрать категорию', callback_data='select_cat')],
        [InlineKeyboardButton(text='Общая информация', callback_data='info')]
    ])
    await message.answer(f"Привет, @{message.from_user.username}? Выбери действие:", reply_markup=markup)