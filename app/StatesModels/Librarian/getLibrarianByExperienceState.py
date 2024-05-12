from aiogram.fsm.state import State, StatesGroup


class GetLibrarianByExperienceState(StatesGroup):
    experience_year = State()
