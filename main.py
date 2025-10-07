import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from app.database.models import init_db, add_user
from config import BOT_TOKEN
from app.utils.logger import logger
from app.handlers import start, generation, menu  
from aiogram.fsm.storage.memory import MemoryStorage



bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(start.router)
dp.include_router(menu.router)
dp.include_router(generation.router)

async def main():
    logger.info("🚀 Бот запускается...")
    await init_db()
    logger.info("✅ База данных инициализирована")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
