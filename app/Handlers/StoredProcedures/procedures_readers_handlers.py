from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
import matplotlib.pyplot as plt

import app.keyboards as kb
from app.Handlers.books_handlers import getBooksDto
from app.Handlers.readers_handlers import inline_categories, getReadersDataframe
from app.Repositories.readersRepository import ReadersRepository
from app.Repositories.typesBookRepository import GenreRepository
from app.StatesModels.Category.getCategoryState import GetCategoryDto
from app.StatesModels.Reader.getReaderByIdState import GetReaderByIdState
from app.Resources.texts.namings import d_ent_func
from app.StatesModels.Reader.getReadersWithBooksByGenreState import GetReadersWithBooksByGenreState
from app.StatesModels.Reader.getTotalCostForReaderState import GetTotalCostForReaderState
from app.handlers import df_empty, answer_dataframe
from settings import path_images

router = Router()


async def init_additional_buttons(message: Message):
    await message.answer("Выберите сущность для работы с дополнительными функциями",
                         reply_markup=kb.additional_buttons)


@router.message(F.text == "Дополнительные функции")
async def create_additional_functions_keyboard(message: Message):
    await message.delete()
    await init_additional_buttons(message)


@router.message(F.text == d_ent_func[0])
async def create_func_readers_keyboard(message: Message):
    await message.delete()
    await message.answer("Список функций", reply_markup=kb.additional_readers_buttons)


@router.message(F.text == "Назад")
async def go_back(message: Message):
    await init_additional_buttons(message)


@router.message(F.text == "Читатели по категории")
async def get_readers_by_category(message: Message, state: FSMContext):
    await state.set_state(GetCategoryDto.name)
    await message.answer("Выберите категорию читателя", reply_markup=await inline_categories())


@router.callback_query(GetCategoryDto.name)
async def get_readers_by_category_name(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(name=callback_query.data)
    data = await state.get_data()
    await state.clear()

    df = await ReadersRepository.getReadersByCategory(int(data["name"]))

    if df.empty:
        await df_empty(df, callback_query.message)
    elif 'Exception' in df.columns:
        await answer_dataframe(df, callback_query.message)
    else:
        df = df.rename(columns={"fk_id_category": "c", "id_reader": "id", "first_name": "name"})
        df.set_index('id', inplace=True)
        await answer_dataframe(df, callback_query.message)


@router.message(F.text == "Читатели с выбранной книгой")
async def get_readers_by_book(message: Message, state: FSMContext):
    await state.set_state(GetReaderByIdState.id_reader)

    df = await getBooksDto()

    await answer_dataframe(df, message)
    await message.answer("Выберите книгу (укажите id)")


@router.message(GetReaderByIdState.id_reader)
async def get_readers_by_book_name(message: Message, state: FSMContext):
    await state.update_data(id_reader=message.text)
    data = await state.get_data()
    await state.clear()

    df = await ReadersRepository.getReadersByBook(int(data["id_reader"]))

    if df.empty:
        await df_empty(df, message)
    else:
        df.set_index('id', inplace=True)
        await answer_dataframe(df, message)


@router.message(F.text == "Читатели с просроченной книгой")
async def get_reader_with_overdue_books(message: Message):
    df = await ReadersRepository.getReadersWithOverdue()
    df.set_index('id', inplace=True)

    plt.figure(figsize=(12, 8))
    plt.bar(df['name'], df['Просрок (в днях)'])
    plt.grid()

    png = path_images + "overdue_books.png"
    plt.savefig(png, dpi=300)

    await message.answer_photo(
        caption='График читателей с просроченной книгой',
        photo=FSInputFile(path=png))


@router.message(F.text == "Читатели с книгой по жанру")
async def get_readers_with_books_by_genre(message: Message, state: FSMContext):
    await state.set_state(GetReadersWithBooksByGenreState.date_start)
    await message.answer("Введите дату начала периода. \nФормат даты: YYYY-MM-DD")


@router.message(GetReadersWithBooksByGenreState.date_start)
async def get_readers_with_books_by_genre_start(message: Message, state: FSMContext):
    await state.update_data(date_start=message.text)
    await state.set_state(GetReadersWithBooksByGenreState.date_end)
    await message.answer("Введите дату конца периода. \nФормат даты: YYYY-MM-DD")


@router.message(GetReadersWithBooksByGenreState.date_end)
async def get_readers_with_books_by_genre_end(message: Message, state: FSMContext):
    await state.update_data(date_end=message.text)
    await state.set_state(GetReadersWithBooksByGenreState.id_genre)

    df = await GenreRepository.getGenre()

    await answer_dataframe(df, message)
    await message.answer("Выберите жанр (укажите id)")


@router.message(GetReadersWithBooksByGenreState.id_genre)
async def get_readers_with_books_by_genre_id(message: Message, state: FSMContext):
    await state.update_data(id_genre=message.text)
    data = await state.get_data()
    await state.clear()

    df = await ReadersRepository.getReadersByGenreOfBookInPeriod(
        int(data['id_genre']), data['date_start'], data['date_end'])

    if df.empty:
        await df_empty(df, message)
    else:
        df.set_index('id', inplace=True)
        await answer_dataframe(df, message)


# Метод с машиной состояний (FSM) для работы с дополнительными функциями
@router.message(F.text == "Общая стоимость за книгу")
async def get_book_price(message: Message, state: FSMContext):
    await state.set_state(GetTotalCostForReaderState.id_reader)

    df = await getReadersDataframe()

    await answer_dataframe(df, message)
    await message.answer("Выберите читателя (укажите id)")


@router.message(GetTotalCostForReaderState.id_reader)
async def get_book_price_reader_id(message: Message, state: FSMContext):
    await state.update_data(id_reader=message.text)
    await state.set_state(GetTotalCostForReaderState.date_last)
    await message.answer("Введите дату. \nФормат даты: YYYY-MM-DD")


@router.message(GetTotalCostForReaderState.date_last)
async def get_book_price_date_last(message: Message, state: FSMContext):
    await state.update_data(date_last=message.text)
    data = await state.get_data()
    await state.clear()

    df = await ReadersRepository.getTotalCost(int(data['id_reader']), data['date_last'])

    if df.empty:
        await df_empty(df, message)
    elif "Exception" in df.columns:
        await answer_dataframe(df, message)
    else:
        df.set_index('id_return_book', inplace=True)
        await answer_dataframe(df, message)
