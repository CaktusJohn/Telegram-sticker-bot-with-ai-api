import asyncio
from aiogram import Router, F
import os
import json
from aiogram.types import Document, Message
from aiogram.fsm.context import FSMContext
from app.services.facemint_service import FacemintService
from app.utils.file_handler import download_user_photo, validate_image
from app.database.models import add_face_detection
from app.states.user_states import UserStates
from datetime import datetime
from app.utils.logger import logger
from aiogram.filters import StateFilter

facemint_service = FacemintService()
router = Router()



# --- Обработчик загрузки фото ---
@router.message(F.document, StateFilter(UserStates.waiting_photo))
async def handle_photo_upload(message: Message, state: FSMContext):
    # 1️⃣ Скачать фото пользователя
    
    file_path = await download_user_photo(message.document, message.from_user.id)

    # 2️⃣ Валидация изображения
    valid, error = await validate_image(file_path)
    if not valid:
        await message.answer(f"❌ Ошибка: {error}\nПопробуйте загрузить другое фото.")
        return

    await message.answer("🔎 Проверяем наличие лиц на фото...")

    # 3️⃣ Формируем публичный URL через Nginx
    filename = os.path.basename(file_path)
    image_url = f"http://195.133.25.216/media/{filename}"
    logger.info(f"Сформирован публичный URL для фото: {image_url}")

    # 4️⃣ Вызов Facemint API для детекции лиц
    result = await facemint_service.faces_from_url(image_url)

    if result['code'] != 0:
        await message.answer("⚠️ Ошибка сервиса. Попробуйте позже.")
        return

    faces_count = result['data']['count']
    faces_data = result['data']['faces']

    if faces_count == 0:
        await message.answer("❌ Лица не найдены. Пожалуйста, загрузите фото с четко видимым лицом.")
        return

    # 5️⃣ Сохраняем результат в базу
    await add_face_detection(
        user_id=message.from_user.id,
        file_path=file_path,
        faces_count=faces_count,
        faces_data=json.dumps(faces_data),
        created_at=datetime.utcnow()
    )

    # 6️⃣ Сохраняем метаданные в JSON
    meta_path = os.path.join(os.path.dirname(file_path), "meta.json")
    meta = {
        "original_path": file_path,
        "faces_detected": True,
        "faces_count": faces_count,
        "faces_data": faces_data,
        "created_at": datetime.utcnow().isoformat()
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # 7️⃣ Обновляем FSM состояние
    await state.set_state(UserStates.photo_validated)
    await message.answer("✅ Фото принято! Теперь выберите категорию шаблона.")

