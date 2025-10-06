from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

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
        "Привет 👋\nВыбери, что хочешь сделать:",
        reply_markup=menu
    )

# --- Обработчики кнопок ---
@router.callback_query(F.data == "create_stickers")
async def create_stickers_callback(callback: CallbackQuery):
    await callback.message.answer("🎨 Начнем создавать твой стикерпак!")
    await callback.answer()  # чтобы Telegram не показывал «часики»

@router.callback_query(F.data == "ref_program")
async def ref_program_callback(callback: CallbackQuery):
    await callback.message.answer("🤝 Здесь будет информация о реферальной программе.")
    await callback.answer()

@router.callback_query(F.data == "try_free")
async def try_free_callback(callback: CallbackQuery):
    await callback.message.answer("💎 Ты получил бесплатную попытку!")
    await callback.answer()

@router.callback_query(F.data == "support")
async def support_callback(callback: CallbackQuery):
    await callback.message.answer("🛠️ Напиши сюда свой вопрос — техподдержка скоро ответит.")
    await callback.answer()

