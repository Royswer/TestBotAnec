from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from config import bot_token
from db_manager import DB

router = Router()
db_manager = DB()

#Случайный анекдот
@router.callback_query(F.data == 'random_anec')
async def callback_handler(callback: CallbackQuery, state: FSMContext):
    joke = db_manager.get_random_anecdot()
    await callback.message.answer(joke)