from aiogram import F, Router
from aiogram.types import Message

from app.Repositories.returningBooksRepository import ReturningBooksRepository
from app.Repositories.typesBookRepository import GenreRepository
from app.Repositories.typesBookRepository import TypesLiteratureRepository
from app.handlers import CRUD_button

router = Router()


@router.message(F.text == "Жанры книг")
async def genres(message: Message):
    df = await GenreRepository.getGenre()

    df.set_index("id_genre", inplace=True)

    await CRUD_button(message, df, "genre")


@router.message(F.text == "Жанры литературы")
async def literatures(message: Message):
    df = await TypesLiteratureRepository.getGenre()

    df.set_index("id_literature_type", inplace=True)

    await CRUD_button(message, df, "literature_type")
