from aiogram.fsm.state import StatesGroup, State


class CreateReturningBooksState(StatesGroup):
    id_issued_book = State()
    date_of_actual = State()