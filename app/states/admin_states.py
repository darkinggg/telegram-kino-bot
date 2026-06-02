from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    waiting_for_movie = State()
    waiting_for_movie_title = State()
    waiting_for_movie_director = State()
    waiting_for_movie_year = State()
    waiting_for_movie_category = State()
    waiting_for_movie_description = State()
    waiting_for_code_to_delete = State()
    waiting_for_broadcast_message = State()