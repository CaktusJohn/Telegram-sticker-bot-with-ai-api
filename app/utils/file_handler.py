import os
from aiogram.types import Document
from PIL import Image

async def download_user_photo(document: Document, user_id: int) -> str:
    """
    Скачивает файл пользователя в tmp/{user_id}/original.{ext}
    """
    # Создаем папку для пользователя
    user_dir = os.path.join("tmp", str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    # Определяем расширение
    ext = document.file_name.split('.')[-1]
    file_path = os.path.join(user_dir, f"original.{ext}")

    # Скачивание файла
    file = await document.bot.get_file(document.file_id)
    file_bytes = await document.bot.download_file(file.file_path)
    with open(file_path, "wb") as f:
        f.write(file_bytes.read())

    return file_path

async def validate_image(file_path: str) -> tuple[bool, str]:
    """
    Проверка формата, размера и разрешения изображения
    Возвращает (True, None) если всё ок, иначе (False, сообщение об ошибке)
    """
    try:
        img = Image.open(file_path)
    except Exception:
        return False, "Невозможно открыть файл как изображение."

    # Проверка формата
    if img.format not in ["JPEG", "PNG"]:
        return False, "Файл должен быть JPEG или PNG."

    # Проверка разрешения
    if min(img.size) < 256:
        return False, "Минимальное разрешение — 256 пикселей по короткой стороне."

    # Проверка соотношения сторон
    if max(img.size) / min(img.size) > 20:
        return False, "Соотношение сторон слишком большое."

    # Проверка размера файла
    if os.path.getsize(file_path) > 10 * 1024 * 1024:
        return False, "Размер файла превышает 10 МБ."

    return True, None
