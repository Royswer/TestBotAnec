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
class DialogStates(StatesGroup):
    waiting_anecdot = State()
    waiting_category_for_anec = State()

#Добавление анекдота
@router.callback_query(F.data == 'add_anec')
async def callback_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите анекдот:")
    await state.set_state(DialogStates.waiting_anecdot)

# Выбор категории для добавленного анекдота
@router.callback_query(F.data.startswith("cat_"))
async def callback_handler(callback: CallbackQuery, state: FSMContext):
    data = callback.data()
    cat_id = int(data.split("_")[1])
    anec_id = (await state.get_data()).get("last_anec_id")
    if anec_id:
        db_manager.add_cats_anecs(cat_id, anec_id)
        await callback.message.answer("Анекдот добавлен в выбранную категорию!")
    await state.clear()

# Обработка ввода анекдота
@router.message(DialogStates.waiting_anecdot)
async def add_anecdot_handler(message: Message, state: FSMContext):
    anec_id = db_manager.add_anec(message.text, message.from_user.id)
    await state.update_data(last_anec_id=anec_id)

    categories = db_manager.select_categories()
    if not categories:
        await message.answer("Нет категорий, добавьте их в базу.")
        await state.clear()
        return

    buttons = [
        [InlineKeyboardButton(text=c['category'], callback_data=f"cat_{c['id']}")]
        for c in categories
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Выберите категорию для анекдота:", reply_markup=markup)