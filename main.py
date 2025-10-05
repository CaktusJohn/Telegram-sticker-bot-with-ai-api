# main.py
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from app.database.models import init_db, add_user
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    is_new = await add_user(message.from_user.id, message.from_user.username)
    if is_new:
        text = "Привет! Ты новый пользователь — получаешь бонусную генерацию 🎁"
    else:
        text = "С возвращением!"
    await message.answer(text)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
