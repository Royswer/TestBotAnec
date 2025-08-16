from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()

@router.callback_query(F.data == 'info')
async def info_handler(callback: CallbackQuery) -> None:
    await callback.answer()

    text = (
        "Я могу отправить вам случайный анекдот (или несколько).\n"
        "Могу отправить анекдот из определённой категории.\n"
        "Также вы можете добавить в меня свой анекдот :)\n"
        "Автор: Денис Дмитриевич"
    )

    await callback.message.answer(text)