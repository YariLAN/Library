from aiogram import F, Router
from aiogram.types import Message

from app.Repositories.librariansRepository import LibrariansRepository
from app.handlers import CRUD_button

router = Router()


@router.message(F.text == "Библиотекари")
async def getLibrarians(message: Message):
    df = await LibrariansRepository.getLibrarians()

    df = df.rename(columns={
        "date_of_birth": "birth",
        "last_name": "last",
        "first_name": "first",
        "date_start_work": "start"})

    #df.set_index('id', inplace=True)

    await CRUD_button(message, df, "ibrarians")
