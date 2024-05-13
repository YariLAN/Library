from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import app.keyboards as kb
from app.Repositories.librariansRepository import LibrariansRepository
from app.StatesModels.Librarian.authLibrarianState import AuthLibrarianDto
from app.handlers import CRUD_button_with_table, librarians_ids, register_role, context
from app.Resources.texts.namings import librarian

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
        register_role[librarian].append(message.from_user.id)
        context.set_connection(librarian)

        print(f"{librarian}: ", register_role[librarian])
        await message.reply("<b>Вы успешно вошли как библиотекарь</b>", parse_mode="HTML")
        await message.answer("Выберите, с чем вы хотите работать", reply_markup=kb.first_part_tables)
