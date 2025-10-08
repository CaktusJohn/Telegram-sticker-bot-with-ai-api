from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from app.states.user_states import UserStates
from app.utils.logger import logger

router = Router()


@router.callback_query(F.data == "create_stickers")
async def create_stickers_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "🎨 Пришлите ваше фото файлом (не сжатое фото). "
        "Поддерживаемые форматы: JPG, PNG. Размер до 10 МБ."
    )
    await state.set_state(UserStates.waiting_photo)

    await callback.answer()

