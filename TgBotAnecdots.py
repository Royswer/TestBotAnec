import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import bot_token
from db_manager import DB

# Создаем бота и диспетчер
dp = Dispatcher()
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

db_manager = DB('test.db')

class DialogStates(StatesGroup):
    waiting_anecdot = State()
    waiting_category_for_anec = State()

# Главное меню
@dp.message(CommandStart())
async def start_cmd(message: Message) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Случайный анекдот', callback_data='random_anec')],
        [InlineKeyboardButton(text='3 анекдота', callback_data='3_anec')],
        [InlineKeyboardButton(text='Добавить анекдот', callback_data='add_anec')],
        [InlineKeyboardButton(text='Выбрать категорию', callback_data='select_cat')],
    ])
    await message.answer(f"Привет, @{message.from_user.username}! Выбери действие:", reply_markup=markup)

# Обработка нажатий кнопок
@dp.callback_query()
async def callback_handler(callback: CallbackQuery, state: FSMContext):
    data = callback.data

    # Случайный анекдот
    if data == 'random_anec':
        joke = db_manager.get_random_anecdot()
        await callback.message.answer(joke)

    # 3 анекдота
    elif data == '3_anec':
        jokes = db_manager.get_random_anecdots(3)
        await callback.message.answer("\n\n".join(jokes))

    # Добавить анекдот
    elif data == 'add_anec':
        await callback.message.answer("Введите анекдот:")
        await state.set_state(DialogStates.waiting_anecdot)

    # Выбор категории для просмотра анекдота
    elif data == 'select_cat':
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

    # Выбор категории для добавленного анекдота
    elif data.startswith("cat_"):
        cat_id = int(data.split("_")[1])
        anec_id = (await state.get_data()).get("last_anec_id")
        if anec_id:
            db_manager.add_cats_anecs(cat_id, anec_id)
            await callback.message.answer("Анекдот добавлен в выбранную категорию!")
        await state.clear()

    # Показ случайного анекдота из выбранной категории
    elif data.startswith("showcat_"):
        cat_id = int(data.split("_")[1])
        joke = db_manager.get_random_anecdot_by_category(cat_id)
        await callback.message.answer(joke)

    await callback.answer()

# Обработка ввода анекдота
@dp.message(DialogStates.waiting_anecdot)
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

# Эхо для всех остальных сообщений
@dp.message()
async def echo_handler(message: Message):
    await message.answer(f'Я тоже так могу: {message.text}')

# Запуск бота
async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())