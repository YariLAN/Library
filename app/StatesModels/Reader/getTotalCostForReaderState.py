from aiogram.fsm.state import StatesGroup, State


class GetTotalCostForReaderState(StatesGroup):
    id_reader = State()
    date_last = State()
    