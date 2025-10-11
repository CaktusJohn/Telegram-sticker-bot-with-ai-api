
import os
from flask import Flask, send_from_directory
from app.utils.logger import logger

# Получаем абсолютный путь к корневой папке проекта
# Это нужно, чтобы Flask точно знал, где искать папку tmp
# __file__ -> media_server.py
# os.path.dirname(__file__) -> /path/to/faceswap_bot
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = os.path.join(PROJECT_ROOT, 'tmp')

app = Flask(__name__)

@app.route("/media/<user_id>/<filename>")
def serve_media(user_id, filename):
    """
    Этот эндпоинт отдает файл для конкретного пользователя.
    Например, запрос /media/12345/original.jpg
    будет искать файл в /path/to/faceswap_bot/tmp/12345/original.jpg
    """
    logger.info(f"Запрос на файл: user_id={user_id}, filename={filename}")
    
    # Проверяем, что в user_id только цифры, а в filename нет ".."
    # Это базовая защита от попыток выйти за пределы папки пользователя
    if not user_id.isdigit() or ".." in filename:
        logger.warning(f"Попытка несанкционированного доступа: user_id={user_id}, filename={filename}")
        return "Forbidden", 403

    user_specific_dir = os.path.join(TMP_DIR, user_id)

    if not os.path.exists(os.path.join(user_specific_dir, filename)):
        logger.error(f"Файл не найден: {os.path.join(user_specific_dir, filename)}")
        return "Not Found", 404

    try:
        return send_from_directory(
            directory=user_specific_dir,
            path=filename,
            as_attachment=False # Важно, чтобы файл открывался в браузере/API
        )
    except Exception as e:
        logger.error(f"Ошибка при отправке файла: {e}")
        return "Server Error", 500

if __name__ == "__main__":
    # Запускаем на 0.0.0.0, чтобы сервер был доступен извне
    # Порт 5001, чтобы не конфликтовать с другими сервисами
    app.run(host='0.0.0.0', port=5001, debug=False)
