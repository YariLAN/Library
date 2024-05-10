from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.Repositories.librariansRepository import LibrariansRepository
from app.StatesModels.Librarian.authLibrarianDto import AuthLibrarianDto
from app.handlers import CRUD_button_with_table, librarians_ids

router = Router()


@router.message(F.text == "Библиотекари")
async def getLibrarians(message: Message):
    df = await LibrariansRepository.getLibrarians()

    df = df.rename(columns={
        "date_of_birth": "birth",
        "last_name": "last",
        "first_name": "first",
        "date_start_work": "start"})

    # df.set_index('id', inplace=True)

    await CRUD_button_with_table(message, df, "ibrarians")


@router.message(AuthLibrarianDto.name)
async def auth_librarian_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    names = message.text.split(" ")

    df = await LibrariansRepository.getLibrarianByName(names[0], names[1], names[2])

    if df.empty:
        await message.reply("<b>Такого библиотекаря не существует ⚠️</b>", parse_mode="HTML")
    else:
        librarians_ids[message.from_user.id] = df["id"].values[0]