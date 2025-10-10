from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.states.user_states import UserStates
from app.keyboards.main import get_categories_keyboard
from app.utils.logger import logger

router = Router()


@router.callback_query(F.data == "try_free")
async def try_free_callback(callback: CallbackQuery, state: FSMContext):
    """
    Starts the template selection process by showing the first page of categories.
    """
    logger.info(f"User {callback.from_user.id} started the 'try_free' flow.")
    
    # Устанавливаем состояние выбора категории
    await state.set_state(UserStates.selecting_category)
    
    # Показываем первую страницу меню категорий
    await callback.message.edit_text(
        "Выберите категорию шаблонов:",
        reply_markup=get_categories_keyboard(page=0)
    )
    await callback.answer()

