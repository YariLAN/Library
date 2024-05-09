from aiogram import F, Router
from aiogram.types import Message

from app.Repositories.returningBooksRepository import ReturningBooksRepository
from app.Repositories.issuedsRepository import IssuedsRepository
from app.handlers import CRUD_button

router = Router()


@router.message(F.text == "Сданные книги")
async def issuedBooks(message: Message):
    df = await IssuedsRepository().getIssueds()

    df = df.rename(columns={"id_issued": "id", "fk_id_reader": "id_reader", "fk_id_book": "id_book"})
    df.set_index("id", inplace=True)

    await CRUD_button(message, df, "issued")


@router.message(F.text == "Принятые от читателей книги")
async def returningBooks(message: Message):
    df = await ReturningBooksRepository().getReturningBooks()

    df = df.rename(columns={"id_return_book": "id", "fk_id_issued_book": "id_issued"})
    df.set_index("id", inplace=True)

    await CRUD_button(message, df, "returning_books")
