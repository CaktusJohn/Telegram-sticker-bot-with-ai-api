
import aiosqlite
from app.database.db import CREATE_USERS_TABLE

DB_PATH = "app/database/database.db"

async def init_db():
    """Создаёт БД и таблицу users при запуске."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_USERS_TABLE)
        await db.commit()


async def add_user(tg_id: int, username: str = None):
    """Добавляет нового пользователя, если его нет в базе."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Проверяем, существует ли пользователь
        check = await db.execute("SELECT tg_id FROM users WHERE tg_id = ?", (tg_id,))
        exists = await check.fetchone()

        if not exists:
            await db.execute(
                "INSERT INTO users (tg_id, username) VALUES (?, ?)",
                (tg_id, username)
            )
            await db.commit()
            return True  # новый пользователь
        return False  # уже есть
