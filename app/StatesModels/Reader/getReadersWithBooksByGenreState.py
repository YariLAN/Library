from aiogram.fsm.state import StatesGroup, State


class GetReadersWithBooksByGenreState(StatesGroup):
    date_start = State()
    date_end = State()
    id_genre = State()
