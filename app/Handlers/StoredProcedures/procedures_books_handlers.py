from aiogram import Router, F
from aiogram.types import Message

import app.keyboards as kb
from app.Repositories.booksRepository import BooksRepository
from app.Resources.texts.namings import d_ent_func
from app.handlers import df_empty, answer_dataframe

router = Router()


@router.message(F.text == d_ent_func[2])
async def create_func_books_keyboard(message: Message):
    await message.delete()
    await message.answer("Список функций", reply_markup=kb.additional_books_buttons)


@router.message(F.text == "Списанные книги")
async def get_written_off_books(message: Message):
    df = await BooksRepository.getWrittenOffBooks()

    if df.empty:
        await df_empty(df, message)
        return

    df.set_index("id", inplace=True)
    await answer_dataframe(df, message)
