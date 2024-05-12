from aiogram.fsm.state import State, StatesGroup


class SetPeriodIssueForGenreState(StatesGroup):
    start_date = State()
    end_date = State()
