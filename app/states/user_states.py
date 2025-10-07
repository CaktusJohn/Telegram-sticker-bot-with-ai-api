from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    waiting_photo = State()       # ждём, пока пользователь отправит фото
    photo_processing = State()    # фото обрабатывается (детекция лиц)
    photo_validated = State()     # фото успешно проверено, можно выбирать категорию
