from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.DbModels.ReturningBook import ReturningBook
from app.Repositories.returningBooksRepository import ReturningBooksRepository
from app.Repositories.issuedsRepository import IssuedsRepository
from app.StatesModels.Returning_book.createReturningBooksState import CreateReturningBooksState
from app.handlers import CRUD_button_with_table, df_empty, answer_dataframe, librarians_ids

router = Router()


async def getDataframeIssueds():
    df = await IssuedsRepository().getIssueds()

    if df.empty:
        return

    df = df.rename(columns={"id_issued": "id", "fk_id_reader": "id_reader", "fk_id_book": "id_book"})
    df.set_index("id", inplace=True)

    return df


@router.message(F.text == "Сданные книги")
async def issuedBooks(message: Message):
    df = await getDataframeIssueds()

    await CRUD_button_with_table(message, df, "issued")


@router.message(F.text == "Принятые от читателей книги")
async def returningBooks(message: Message):
    df = await ReturningBooksRepository().getReturningBooks()

    df = df.rename(columns={"id_return_book": "id", "fk_id_issued_book": "id_issued"})
    df.set_index("id", inplace=True)

    await CRUD_button_with_table(message, df, "returning_books")


@router.callback_query(F.data.startswith("returning_books"))
async def CRUD_returning_books(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data.endswith("add"):
        df = await getDataframeIssueds()

        if df.empty:
            await df_empty(df, callback_query.message)
            return
        else:
            await answer_dataframe(df, callback_query.message)

        await callback_query.message.reply("Выберите книгу id из списка сданных книг")
        await state.set_state(CreateReturningBooksState.id_issued_book)


@router.message(CreateReturningBooksState.id_issued_book)
async def returning_books_add(message: Message, state: FSMContext):
    await state.update_data(id_issued_book=message.text)
    await state.set_state(CreateReturningBooksState.date_of_actual)
    await message.answer("Укажите дату возвращения книги. \nФормат: YYYY-MM-DD")


@router.message(CreateReturningBooksState.date_of_actual)
async def returning_books_add_date(message: Message, state: FSMContext):
    await state.update_data(date_of_actual=message.text)
    data = await state.get_data()
    await state.clear()

    result = await ReturningBooksRepository().createReturningBooks(
        ReturningBook(
            int(librarians_ids[message.from_user.id]),
            int(data["id_issued_book"]),
            data["date_of_actual"]))

    if result:
        await message.answer(f"Книга с id среди сданных {data['id_issued_book']} добавлена")
    else:
        await message.answer(f"Добавить не удалось. {result}")

    await returningBooks(message)
