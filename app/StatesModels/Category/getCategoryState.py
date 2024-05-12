from aiogram.fsm.state import StatesGroup, State


class GetCategoryDto(StatesGroup):
    name = State()
