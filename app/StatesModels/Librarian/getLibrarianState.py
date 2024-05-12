from aiogram.fsm.state import State, StatesGroup


class GetLibrarianState(StatesGroup):
    id_librarian = State()
