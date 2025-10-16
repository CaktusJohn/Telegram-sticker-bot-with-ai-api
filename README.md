Faceswap sticker bot
## Структура проекта

```
faceswap_bot/
├── main.py                    # Точка входа приложения
├── config.py                  # Конфигурация и переменные окружения
├── requirements.txt           # Зависимости проекта
├── .env                       # Переменные окружения
├── database.db                # SQLite база данных
├── temp_files/                # Временные файлы пользователей
└── app/
    ├── handlers/              # Обработчики команд и сообщений
    │   ├── start.py           # Команда /start, регистрация
    │   ├── menu.py            # Главное меню
    │   ├── payment.py         # Обработка платежей Stars
    │   ├── generation.py      # Генерация face swap
    │   ├── referral.py        # Реферальная система
    │   └── support.py         # Техподдержка
    ├── keyboards/             # Клавиатуры и кнопки
    │   └── main.py            # Все клавиатуры
    ├── database/              # Работа с базой данных
    │   ├── db.py              # Подключение и инициализация
    │   └── models.py          # Модели данных и запросы
    ├── services/              # Бизнес-логика
    │   ├── user_service.py    # Работа с пользователями
    │   ├── payment_service.py # Логика платежей
    │   ├── facemint_service.py # Интеграция с Facemint API
    │   └── referral_service.py # Реферальная логика
    └── utils/                 # Вспомогательные функции
        └── logger.py          # Настройка логирования
```
