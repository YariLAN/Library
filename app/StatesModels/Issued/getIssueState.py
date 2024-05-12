from aiogram.fsm.state import StatesGroup, State


class GetIssueState(StatesGroup):
    start_date = State()
    end_date = State()
