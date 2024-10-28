# modules/feedback.py

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db.feedback import add_feedback


class FeedbackState(StatesGroup):
    waiting_for_feedback = State()


async def receive_feedback(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    feedback_text = message.text.strip()

    if feedback_text:
        add_feedback(user_id, feedback_text)
        await message.answer("Спасибо за ваш фидбэк!")
        await state.clear()
    else:
        await message.answer("Отзыв не может быть пустым. Попробуйте еще раз.")


async def handle_feedback_if_active(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == FeedbackState.waiting_for_feedback.state:
        await receive_feedback(message, state)
        return True
    return False


def register_feedback_handlers(dp):
    dp.message.register(receive_feedback, FeedbackState.waiting_for_feedback)
