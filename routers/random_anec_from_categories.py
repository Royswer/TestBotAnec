from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from config import bot_token
from database.db_manager import DB

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


