from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import app.keyboards as kb
from app.Repositories.typesBookRepository import GenreRepository
from app.Resources.texts.namings import d_ent_func
from app.StatesModels.Issued.setPeriodIssueForGenreState import SetPeriodIssueForGenreState
from app.handlers import df_empty, answer_dataframe

router = Router()


@router.message(F.text == d_ent_func[3])
async def create_func_genre_keyboard(message: Message):
    await message.delete()
    await message.answer("Список функций", reply_markup=kb.additional_genre_buttons)


@router.message(F.text == "Популярные жанры")
async def get_popular_genres(message: Message, state: FSMContext):
    await state.set_state(SetPeriodIssueForGenreState.start_date)
    await message.answer("Введите начало периода. \nФормат: YYYY-MM-DD")


@router.message(SetPeriodIssueForGenreState.start_date)
async def get_popular_genres_start_date(message: Message, state: FSMContext):
    await state.update_data(start_date=message.text)
    await state.set_state(SetPeriodIssueForGenreState.end_date)
    await message.answer("Введите конец периода. \nФормат: YYYY-MM-DD")


@router.message(SetPeriodIssueForGenreState.end_date)
async def get_popular_genres_end_date(message: Message, state: FSMContext):
    await state.update_data(end_date=message.text)
    data = await state.get_data()
    await state.clear()

    df = await GenreRepository.getPopularGenres(data["start_date"], data["end_date"])

    if df.empty:
        await df_empty(df, message)
        return

    await answer_dataframe(df, message)
