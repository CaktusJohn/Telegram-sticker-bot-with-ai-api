from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove
router = Router()

# --- Меню с inline-кнопками ---
menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="✨ Создать стикерпак", callback_data="create_stickers"),
        InlineKeyboardButton(text="🤝 Реферальная программа", callback_data="ref_program")
    ],
    [
        InlineKeyboardButton(text="💎 Попробовать бесплатно", callback_data="try_free"),
        InlineKeyboardButton(text="🛠️ Техподдержка", callback_data="support")
    ]
])

# --- Команда /start ---
@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer(
        "Привет 👋\n Это стикер бот",
        reply_markup=ReplyKeyboardRemove() 
    )
    await message.answer(
        "Вот твоё меню:",
        reply_markup=menu  # ← показываем inline-кнопки
    )

