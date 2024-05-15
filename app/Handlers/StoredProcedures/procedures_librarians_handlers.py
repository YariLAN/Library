import pandas as pd
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, InputFile
import matplotlib.pyplot as plt

import app.keyboards as kb
from app.Repositories.librariansRepository import LibrariansRepository
from app.StatesModels.Issued.getIssueState import GetIssueState
from app.StatesModels.Librarian.getLibrarianByExperienceState import GetLibrarianByExperienceState
from app.StatesModels.Librarian.getLibrarianState import GetLibrarianState
from app.Resources.texts.namings import d_ent_func
from app.handlers import df_empty, answer_dataframe
from settings import path_images

router = Router()


@router.message(F.text == d_ent_func[1])
async def create_func_librarians_keyboard(message: Message):
    await message.delete()
    await message.answer("Список функций", reply_markup=kb.additional_librarians_buttons)


@router.message(F.text == "Выработок библиотекарей")
async def get_librarians_work(message: Message, state: FSMContext):
    await state.set_state(GetIssueState.start_date)
    await message.answer("Укажите начало периода. \nФормат даты: YYYY-MM-DD")


@router.message(GetIssueState.start_date)
async def get_librarians_work_start_date(message: Message, state: FSMContext):
    await state.update_data(start_date=message.text)
    await state.set_state(GetIssueState.end_date)
    await message.answer("Введите дату окончания периода. \nФормат даты: YYYY-MM-DD")


async def create_plot(message: Message, df: pd.DataFrame, data):
    plt.figure(figsize=(12, 5))
    plt.plot(df["name"], df["num_issued"], label="Списанные книги")
    plt.plot(df["name"], df["num_received"], label="Полученные книги")

    plt.grid()
    plt.tight_layout()
    plt.legend()

    png = path_images + "librarians_work.png"
    plt.savefig(png, dpi=300)

    await message.answer_photo(
        caption=f'Выработка каждого библиотекаря за {data["start_date"]} - {data["end_date"]}',
        photo=FSInputFile(png))


@router.message(GetIssueState.end_date)
async def get_librarians_work_end_date(message: Message, state: FSMContext):
    await state.update_data(end_date=message.text)
    data = await state.get_data()
    await state.clear()

    df = await LibrariansRepository.getLibrariansWork(data["start_date"], data["end_date"])

    if df.empty:
        await df_empty(df, message)
    else:
        await create_plot(message, df, data)


@router.message(F.text == "Стаж")
async def get_experience(message: Message, state: FSMContext):
    await state.set_state(GetLibrarianByExperienceState.experience_year)
    await message.answer("Введите срок стажа")


@router.message(GetLibrarianByExperienceState.experience_year)
async def get_experience_year(message: Message, state: FSMContext):
    await state.update_data(experience_year=message.text)
    data = await state.get_data()
    await state.clear()

    df = await LibrariansRepository.getExperience(data["experience_year"])

    if df.empty:
        await df_empty(df, message)
    else:
        await answer_dataframe(df, message)


@router.message(F.text == "Число обслуженных категорий")
async def get_count_categories(message: Message, state: FSMContext):
    await state.set_state(GetLibrarianState.id_librarian)

    df = await LibrariansRepository.getLibrarians()

    if df.empty:
        await df_empty(df, message)
        return

    df.set_index("id", inplace=True)
    df = df.rename(columns={"date_of_birth": "birth", "date_start_work": "start"})

    await answer_dataframe(df, message)
    await message.reply("Выберите библиотекаря (укажите его ID)")


@router.message(GetLibrarianState.id_librarian)
async def get_count_categories_id(message: Message, state: FSMContext):
    await state.update_data(id_librarian=message.text)
    data = await state.get_data()
    await state.clear()

    df = await LibrariansRepository.getCountCategory(int(data["id_librarian"]))

    if df.empty:
        await df_empty(df, message)
        return

    plt.figure(figsize=(12, 8))
    plt.pie(df['count_category'], labels=df['name_category'], autopct='%1.1f%%', startangle=140)
    plt.legend(df['name_category'], title="Категории", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    png = path_images + "count_categories.png"
    plt.savefig(png, dpi=300)

    await message.answer_photo(
        caption=f'Круговая диаграмма обслуженных категорий читателей для id: {data["id_librarian"]}',
        photo=FSInputFile(path=png))
