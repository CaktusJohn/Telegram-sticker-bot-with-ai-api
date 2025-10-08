# app/handlers/admin.py
from aiogram import Router
from aiogram.filters import BaseFilter, Command, CommandObject
from aiogram.types import Message
from config import ADMIN_ID
from app.utils.logger import logger
from app.services.facemint_service import FacemintService, FacemintError
import json

# 1. Создаём кастомный фильтр для проверки на админа
class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == ADMIN_ID

# 2. Создаём роутер, который будет использовать этот фильтр для ВСЕХ своих хэндлеров
router = Router()
router.message.filter(IsAdmin())

# Инициализируем сервис
facemint_service = FacemintService()

# 3. Создаём "пробную" команду, чтобы проверить, что всё работает
@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Простая команда для проверки прав администратора."""
    await message.answer("👑 Добро пожаловать, администратор!")

@router.message(Command("test_faces"))
async def cmd_test_faces(message: Message, command: CommandObject):
    """
    Тестирует эндпоинт детекции лиц.
    Пример: /test_faces https://example.com/image.jpg
    """
    if not command.args:
        await message.answer("❌ Укажите URL изображения после команды.\n"
                             "Пример: `/test_faces https://example.com/image.jpg`")
        return

    url = command.args
    await message.answer(f"⏳ Выполняю запрос детекции лиц для URL:\n{url}")
    
    try:
        logger.debug(f"Admin command /test_faces called with url: {url}")
        result = await facemint_service.faces_from_url(url)
        
        # Форматируем ответ для красивого вывода
        pretty_result = json.dumps(result, indent=2, ensure_ascii=False)
        
        await message.answer(f"✅ Успешный ответ от API:\n<pre>{pretty_result[:3000]}</pre>", parse_mode="HTML")

    except FacemintError as e:
        logger.error(f"Admin command /test_faces failed: {e}")
        await message.answer(f"🔥 Ошибка API Facemint:\n`{str(e)[:1000]}`")
    except Exception as e:
        logger.error(f"Unexpected error in /test_faces: {e}")
        await message.answer(f"🤯 Непредвиденная ошибка:\n`{str(e)[:1000]}`")


@router.message(Command("test_status"))
async def cmd_test_status(message: Message, command: CommandObject):
    """
    Тестирует эндпоинт получения статуса задачи.
    Пример: /test_status mock_task_123
    """
    if not command.args:
        await message.answer("❌ Укажите ID задачи после команды.\n"
                             "Пример: `/test_status mock_task_123`")
        return

    task_id = command.args
    await message.answer(f"⏳ Проверяю статус задачи `{task_id}`...")

    try:
        result = await facemint_service.get_task_info(task_id)
        pretty_result = json.dumps(result, indent=2, ensure_ascii=False)
        await message.answer(f"✅ Статус задачи:\n<pre>{pretty_result}</pre>", parse_mode="HTML")

    except FacemintError as e:
        await message.answer(f"🔥 Ошибка API Facemint:\n`{str(e)[:1000]}`")
    except Exception as e:
        await message.answer(f"🤯 Непредвиденная ошибка:\n`{str(e)[:1000]}`")


@router.message(Command("test_task"))
async def cmd_test_task(message: Message, command: CommandObject):
    """
    Тестирует эндпоинт создания задачи.
    Пример: /test_task <media_url> <face_url>
    """
    if not command.args or len(command.args.split()) != 2:
        await message.answer("❌ Укажите два URL после команды: media_url и face_url.\n"
                             "Пример: `/test_task url1 url2`")
        return

    media_url, face_url = command.args.split()
    await message.answer(f"⏳ Создаю тестовую задачу...")

    try:
        # ВАЖНО: payload должен соответствовать документации API Facemint
        payload = {
            "type": "gif",
            "media_url": media_url,
            "callback_url": "https://example.com/callback",  # API требует синтаксически верный URL, даже если он не используется
            "swap_list": [
                {
                    # from_face опускаем, чтобы заменять все лица в медиа
                    "to_face": face_url
                }
            ]
        }
        result = await facemint_service.create_face_swap_task(payload)
        pretty_result = json.dumps(result, indent=2, ensure_ascii=False)
        await message.answer(f"✅ Задача создана:\n<pre>{pretty_result[:3000]}</pre>", parse_mode="HTML")

    except FacemintError as e:
        await message.answer(f"🔥 Ошибка API Facemint:\n`{str(e)[:1000]}`")
    except Exception as e:
        await message.answer(f"🤯 Непредвиденная ошибка:\n`{str(e)[:1000]}`")


logger.info("Админ-хэндлеры настроены.")
