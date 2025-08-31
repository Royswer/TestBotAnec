from aiogram import Bot, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import bot_token, admin_channel_chat_id
from database.db_manager import DB


bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
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

# Обработка ввода анекдота
@router.message(DialogStates.waiting_anecdot)
async def add_anecdot_handler(message: Message, state: FSMContext):
    anec_id = db_manager.add_anec('Модерация', message.text, message.from_user.id)
    await state.update_data(last_anec_id=anec_id)
    await state.update_data(last_anec_text=message.text)

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

# Выбор категории для добавленного анекдота
@router.callback_query(F.data.startswith("cat_"))
async def callback_handler(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    cat_id = int(data.split("_")[1])
    anec_id = (await state.get_data()).get("last_anec_id")
    anec_text = (await state.get_data()).get("last_anec_text")
    if anec_id:
        db_manager.add_cats_anecs(cat_id, anec_id)
        await callback.message.answer("Анекдот отправлен на проверку, спасибо.")
    await state.clear()
    
    #Отправить админу анекдот на проверку
    buttons = [
        [InlineKeyboardButton(text='Одобрить', callback_data=f'check_confirm_{anec_id}')],
        [InlineKeyboardButton(text='Отклонить', callback_data=f'check_reject_{anec_id}')]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(admin_channel_chat_id, f'Добавлен анекдот:\n{anec_text}', reply_markup=markup)

#Ответ от админа
@router.callback_query(F.data.startswith('check_'))
async def callback_handler(callback: CallbackQuery, state: FSMContext):
    status = callback.data.split('_')[1]
    anec_id = callback.data.split('_')[2]

    if status == 'confirm':
        anec_id = db_manager.update_status_anec(anec_id=anec_id, status='Одобрено')
    
    if status == 'reject':
       anec_id = db_manager.update_status_anec(anec_id=anec_id, status='Отклонено')