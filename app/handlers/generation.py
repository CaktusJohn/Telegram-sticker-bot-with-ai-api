from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from app.keyboards.main import get_categories_keyboard, get_template_navigation_keyboard
from app.states.user_states import UserStates
from app.utils.logger import logger

router = Router()

# ... (комментарии-планы)

# --- Обработчик для пагинации категорий ---
@router.callback_query(F.data.startswith("cat_page_"), StateFilter(UserStates.selecting_category))
async def handle_category_pagination(callback: CallbackQuery):
    page = int(callback.data.split("_")[-1])
    await callback.message.edit_reply_markup(
        reply_markup=get_categories_keyboard(page=page)
    )
    await callback.answer()


# Словарь соотнесения категорий и стикерпаков
STICKER_PACKS = {
    "🎬 Фильмы и сериалы": "NBstickeriaBrat",
    "🎭 Мемы и приколы": "MemeS1ick3r",
    "💼 Работа и офис": "PutInPacky",
}

# --- Обработчик выбора категории ---
@router.callback_query(F.data.startswith("cat_select_"), StateFilter(UserStates.selecting_category))
async def handle_category_selection(callback: CallbackQuery, state: FSMContext):
    print(f"DEBUG: handle_category_selection triggered! Current state: {await state.get_state()}") # Debug print
    category_name = callback.data.replace("cat_select_", "")
    pack_name = STICKER_PACKS.get(category_name)

    if not pack_name:
        await callback.answer("Для этой категории шаблоны еще не добавлены.", show_alert=True)
        return

    await callback.message.edit_text(f"⏳ Загружаю шаблоны для категории '{category_name}'...")

    try:
        # Final solution: Create a dedicated aiohttp session to make a raw request,
        # completely bypassing any aiogram models or session internals.
        import aiohttp
        from aiogram.types import Sticker

        api_url = f"https://api.telegram.org/bot{callback.bot.token}/getStickerSet"
        payload = {"name": pack_name}
        
        async with aiohttp.ClientSession() as http_session:
            async with http_session.post(api_url, json=payload) as response:
                response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                sticker_set_dict = await response.json()

        if not sticker_set_dict.get('ok'):
            raise Exception(f"Telegram API error: {sticker_set_dict.get('description')}")

        # Manually parse the dictionary to get the list of sticker data
        stickers_data = sticker_set_dict.get('result', {}).get('stickers', [])

        if not stickers_data:
            await callback.message.edit_text("В этой категории пока нет шаблонов.")
            return

        # Convert the raw sticker dicts into aiogram Sticker objects
        stickers = [Sticker(**sticker_data) for sticker_data in stickers_data]
        
        await state.update_data(
            templates=[s.file_id for s in stickers],
            template_page=0,
            current_category=category_name
        )
        await state.set_state(UserStates.selecting_template)

        await callback.message.delete()
        await callback.message.answer_sticker(
            sticker=stickers[0].file_id,
            reply_markup=get_template_navigation_keyboard(
                page=0,
                total_pages=len(stickers),
                category_id=category_name
            )
        )

    except Exception as e:
        logger.error(f"Не удалось получить стикерпак {pack_name}: {e}")
        await callback.message.edit_text("Не удалось загрузить шаблоны. Попробуйте другую категорию.")
    
    await callback.answer()


# --- Обработчики для навигации по шаблонам ---

@router.callback_query(F.data == "back_to_categories", StateFilter(UserStates.selecting_template))
async def back_to_categories(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.selecting_category)
    await callback.message.delete()
    await callback.message.answer(
        "Выберите категорию шаблонов:",
        reply_markup=get_categories_keyboard(page=0)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("tpl_page_"), StateFilter(UserStates.selecting_template))
async def handle_template_selection(callback: CallbackQuery, state: FSMContext):
    print(f"DEBUG: handle_template_selection callback received! Current state: {await state.get_state()}") # Debug print
    print(f"DEBUG: handle_template_pagination triggered! Current state: {await state.get_state()}") # Debug print
    page = int(callback.data.split("_")[-1])
    
    data = await state.get_data()
    templates = data.get("templates", [])
    current_category = data.get("current_category", "")
    
    if not templates:
        await callback.answer("Произошла ошибка, шаблоны не найдены.", show_alert=True)
        return

    new_sticker_id = templates[page]
    
    new_keyboard = get_template_navigation_keyboard(
        page=page,
        total_pages=len(templates),
        category_id=current_category
    )
    
    # Удаляем старое сообщение со стикером
    await callback.message.delete()

    # Присылаем новое с обновленным стикером и клавиатурой
    await callback.message.answer_sticker(
        sticker=new_sticker_id,
        reply_markup=new_keyboard
    )

    await state.update_data(template_page=page) # Update the page in state
    await callback.answer()


# --- Обработчик ВЫБОРА шаблона ---
@router.callback_query(F.data.startswith("tpl_select_"), StateFilter(UserStates.selecting_template))
async def handle_template_confirm(callback: CallbackQuery, state: FSMContext):
    """
    Обрабатывает нажатие кнопки "✅ Выбрать этот шаблон".
    """
    data = await state.get_data()
    templates = data.get("templates", [])
    page = data.get("template_page", 0)
    
    if not templates:
        await callback.answer("Произошла ошибка, шаблоны не найдены.", show_alert=True)
        return

    selected_template_id = templates[page]
    
    # Сохраняем выбранный шаблон в FSM
    await state.update_data(selected_template_id=selected_template_id)
    
    # Переводим пользователя в состояние ожидания фото
    await state.set_state(UserStates.waiting_photo)
    
    await callback.message.delete()
    await callback.message.answer(
        "Отлично! Теперь, пожалуйста, пришлите ваше фото файлом (не сжатое изображение)."
    )
    await callback.answer()


# --- Обработчик загрузки фото (после выбора шаблона) ---
@router.message(F.document, StateFilter(UserStates.waiting_photo))
async def handle_photo_upload(message: Message, state: FSMContext):
    import os
    import json
    # 1️⃣ Скачать фото пользователя
    from app.utils.file_handler import download_user_photo, validate_image
    file_path = await download_user_photo(message.document, message.from_user.id)

    # 2️⃣ Валидация изображения
    valid, error = await validate_image(file_path)
    if not valid:
        await message.answer(f"❌ Ошибка: {error}\nПопробуйте загрузить другое фото.")
        return

    await message.answer("🔎 Проверяем наличие лиц на фото...")

    # 3️⃣ Формируем публичный URL
    from config import MEDIA_HOST
    user_id = message.from_user.id
    filename = os.path.basename(file_path)
    image_url = f"{MEDIA_HOST}/media/{user_id}/{filename}"
    logger.info(f"Сформирован публичный URL для фото: {image_url}")

    # 4️⃣ Вызов Facemint API для детекции лиц
    from app.services.facemint_service import FacemintService
    facemint_service = FacemintService()
    result = await facemint_service.faces_from_url(image_url)

    if result.get('code') != 0:
        await message.answer("⚠️ Ошибка сервиса. Попробуйте позже.")
        return

    faces_count = result.get('data', {}).get('count', 0)

    if faces_count == 0:
        await message.answer("❌ Лица не найдены. Пожалуйста, загрузите фото с четко видимым лицом.")
        return

    # 5️⃣ Сохраняем результат в базу и метаданные
    from app.database.models import add_face_detection
    from datetime import datetime
    await add_face_detection(
        user_id=message.from_user.id,
        file_path=file_path,
        faces_count=faces_count,
        faces_data=json.dumps(result.get('data', {}).get('faces', [])),
        created_at=datetime.utcnow()
    )

    meta_path = os.path.join(os.path.dirname(file_path), "meta.json")
    meta = {
        "original_path": file_path,
        "faces_detected": True,
        "faces_count": faces_count,
        "faces_data": result.get('data', {}).get('faces', []),
        "created_at": datetime.utcnow().isoformat()
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    # 6️⃣ Сохраняем путь к фото в FSM для дальнейшей генерации
    await state.update_data(user_photo_path=file_path)
    
    # 7️⃣ Теперь, когда фото загружено и валидировано, запускаем генерацию
    # (Этот шаг будет реализован в следующем обработчике)
    await message.answer("✅ Фото принято! Начинаю генерацию...")
    # TODO: Вызвать функцию генерации здесь
    await state.clear() # Сбросить состояние после обработки