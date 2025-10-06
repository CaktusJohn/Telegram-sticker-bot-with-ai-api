from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Кнопки меню
main_menu = ReplyKeyboardMarkup(
   keyboard = [
    [
        KeyboardButton(text="✨ Создать стикерпак"),
        KeyboardButton(text="🤝 Реферальная программа")
    ],
    [
        KeyboardButton(text="💎 Попробовать бесплатно"),
        KeyboardButton(text="🛠️ Техподдержка")
    ]
],
    resize_keyboard=True,  # чтобы кнопки подгонялись под экран
)
