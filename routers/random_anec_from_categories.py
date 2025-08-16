import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import bot_token
from db_manager import DB

router = Router()
db_manager = DB()

#Обработка нажатий кнопок
@router.callback_query(F.data == 'select_cat')
async def callback_handler(callback: CallbackQuery, state: FSMContext):
    data = callback.data

    # Выбор категории для просмотра анекдота
    categories = db_manager.select_categories()
    if not categories:
        await callback.message.answer("Категорий пока нет.")
    else:
        buttons = [
            [InlineKeyboardButton(text=c['category'], callback_data=f"showcat_{c['id']}")]
            for c in categories
        ]
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.answer("Выберите категорию:", reply_markup=markup)


@router.callback_query(F.data.startswith("showcat_"))
async def callback_handler(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    # Показ случайного анекдота из выбранной категории
    cat_id = int(data.split("_")[1])
    joke = db_manager.get_random_anecdot_by_category(cat_id)
    await callback.message.answer(joke)
    await callback.answer()


