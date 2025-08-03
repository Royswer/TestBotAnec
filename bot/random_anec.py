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

#Случайный анекдот
@router.callback_query(F.data == 'random_anec')
async def callback_handler(callback: CallbackQuery, state: FSMContext):
    joke = db_manager.get_random_anecdot()
    await callback.message.answer(joke)