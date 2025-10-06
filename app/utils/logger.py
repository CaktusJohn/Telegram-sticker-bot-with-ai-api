from loguru import logger
import sys
from pathlib import Path

# Папка для логов
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Настраиваем логгер
logger.remove()  # Убираем стандартный вывод

# Вывод в консоль (INFO и выше)
logger.add(sys.stdout, level="INFO", format="<green>{time}</green> | <level>{message}</level>")

# Запись в файл (DEBUG и выше)
logger.add(
    LOG_DIR / "bot.log",
    level="DEBUG",
    rotation="10 MB",   # новый файл каждые 10 МБ
    retention="10 days", # храним 10 дней
    compression="zip",   # старые архивируются
    format="{time} | {level} | {message}"
)
