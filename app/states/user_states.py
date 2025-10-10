from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    waiting_photo = State()       # ждём, пока пользователь отправит фото
    photo_processing = State()    # фото обрабатывается (детекция лиц)
    photo_validated = State()     # фото успешно проверено, можно выбирать категорию
    waiting_template_selection = State() # ждём, пока пользователь ответит на стикер-шаблон
    selecting_template = State()      # пользователь находится в меню выбора конкретного шаблона (пагинация)
    selecting_category = State()      # пользователь находится в меню выбора категории
