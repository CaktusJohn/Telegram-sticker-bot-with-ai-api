from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню
menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Попробовать бесплатно", callback_data="try_free")],
    [InlineKeyboardButton(text="Создать реф. ссылку", callback_data="ref_program")],
    [InlineKeyboardButton(text="Техподдержка", callback_data="support")]
])

from aiogram.utils.keyboard import InlineKeyboardBuilder

# Категории шаблонов из схемы
CATEGORIES = [
    "😀 Эмоции и реакции", "🎭 Мемы и приколы", "🎬 Фильмы и сериалы",
    "🎵 Музыка и танцы", "🏆 Спорт", "🎮 Игры",
    "💼 Работа и офис", "🎉 Праздники"
]

def get_categories_keyboard(page: int = 0, items_per_page: int = 4):
    builder = InlineKeyboardBuilder()
    start_index = page * items_per_page
    end_index = start_index + items_per_page
    
    # Рассчитываем общее количество страниц
    total_pages = (len(CATEGORIES) + items_per_page - 1) // items_per_page

    # Добавляем кнопки для категорий на текущей странице
    for category in CATEGORIES[start_index:end_index]:
        builder.button(text=category, callback_data=f"cat_select_{category}")
    
    # Создаем кнопки навигации
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text=f"⬅️ Назад ({page}/{total_pages})", callback_data=f"cat_page_{page-1}"))
    if end_index < len(CATEGORIES):
        nav_buttons.append(InlineKeyboardButton(text=f"Вперед ({page+2}/{total_pages}) ➡️", callback_data=f"cat_page_{page+1}"))
    
    # Выстраиваем кнопки в ряды
    builder.adjust(1) # По одной кнопке категории в ряду
    if nav_buttons:
        builder.row(*nav_buttons) # Кнопки навигации в одном ряду
        
    return builder.as_markup()


def get_template_navigation_keyboard(page: int, total_pages: int, category_id: str):
    builder = InlineKeyboardBuilder()
    
    # Ряд 1: Навигация ⬅️ 1/10 ➡️
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton(text="⬅️", callback_data=f"tpl_page_{page-1}"))
    
    nav_row.append(InlineKeyboardButton(text=f"{page+1}/{total_pages}", callback_data="noop")) # Кнопка-счетчик

    if page < total_pages - 1:
        nav_row.append(InlineKeyboardButton(text="➡️", callback_data=f"tpl_page_{page+1}"))

    if nav_row:
        builder.row(*nav_row)

    # Ряд 2: Выбор шаблона
    builder.row(InlineKeyboardButton(text="✅ Выбрать этот шаблон", callback_data=f"tpl_select_{page}"))

    # Ряд 3: Назад к категориям
    builder.row(InlineKeyboardButton(text="⬅️ Назад к категориям", callback_data="back_to_categories"))

    return builder.as_markup()

# Клавиатура для состояния "фото загружено"
photo_validated_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Категории стикеров", callback_data="select_category")],
    [InlineKeyboardButton(text="Мои стикерпаки", callback_data="my_stickerpacks")],
    [InlineKeyboardButton(text="Загрузить другой файл", callback_data="upload_another_photo")],
    [InlineKeyboardButton(text="Назад в главное меню", callback_data="main_menu")]
])
