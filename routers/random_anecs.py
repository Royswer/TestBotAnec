from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from config import bot_token
from db_manager import DB

router = Router()
db_manager = DB()

#Случайный анекдот
@router.callback_query(F.data == '3_anec')
async def callback_handler(callback: CallbackQuery, state: FSMContext):
    jokes = db_manager.get_random_anecdots(3)
    await callback.message.answer("\n\n".join(jokes))