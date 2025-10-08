from datetime import datetime
import aiosqlite
from app.database.db import (
    CREATE_USERS_TABLE,
    CREATE_FACE_DETECTIONS_TABLE,
    CREATE_TEMP_FILES_TABLE,
)

DB_PATH = "app/database/database.db"


async def init_db():
    """Создаёт БД и все необходимые таблицы при запуске."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_USERS_TABLE)
        await db.execute(CREATE_TEMP_FILES_TABLE)
        await db.execute(CREATE_FACE_DETECTIONS_TABLE)
        await db.commit()


async def add_user(tg_id: int, username: str = None):
    """Добавляет нового пользователя, если его нет в базе."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Проверяем, существует ли пользователь
        check = await db.execute("SELECT tg_id FROM users WHERE tg_id = ?", (tg_id,))
        exists = await check.fetchone()

        if not exists:
            await db.execute(
                "INSERT INTO users (tg_id, username) VALUES (?, ?)", (tg_id, username)
            )
            await db.commit()
            return True  # новый пользователь
        return False  # уже есть


async def add_face_detection(
    user_id: int, file_path: str, faces_count: int, faces_data: str, created_at: datetime
):
    query = """
    INSERT INTO face_detections (user_id, file_path, faces_count, faces_data, created_at)
    VALUES (?, ?, ?, ?, ?)
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            query, (user_id, file_path, faces_count, faces_data, created_at)
        )
        await db.commit()