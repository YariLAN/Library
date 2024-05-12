from aiogram.fsm.state import StatesGroup, State


class CreateReaderDto(StatesGroup):
    name = State()
    category = State()
    address = State()
    phone = State()
    email = State()
