from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove
from app.keyboards.main import menu

router = Router()

# --- Команда /start ---
@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer(
        "Привет 👋\nЭто face-swap бот, который переносит твое лицо на любой стикер.\n\nДля старта нажми 'Попробовать бесплатно' или выбери другую опцию.",
        reply_markup=menu
    )

