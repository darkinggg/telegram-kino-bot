from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    waiting_for_movie = State()
    waiting_for_code_to_delete = State()
    waiting_for_broadcast_message = State()