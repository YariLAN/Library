from aiogram.fsm.state import StatesGroup, State


class GetReaderByIdState(StatesGroup):
    id_reader = State()
