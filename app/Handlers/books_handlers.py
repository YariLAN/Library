from aiogram import F, Router
from aiogram.types import Message

from app.Repositories.booksRepository import BooksRepository
from app.handlers import CRUD_button

router = Router()


@router.message(F.text == "Книги")
async def getReaders(message: Message):
    df = await BooksRepository.getBooks()

    df = df.rename(columns={"fk_id_genre": "gen", "id_book": "id", "fk_id_literature_type": "type", "name_book": "name"})

    df.set_index('id', inplace=True)

    await CRUD_button(message, df, "books")
