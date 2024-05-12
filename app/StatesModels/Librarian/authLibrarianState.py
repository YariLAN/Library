from aiogram.fsm.state import StatesGroup, State


class AuthLibrarianDto(StatesGroup):
    name = State()
