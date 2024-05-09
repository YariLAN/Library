import pandas as pd
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram import F, Router

import app.keyboards as kb
from app.Repositories.categoriesRepository import CategoriesRepository
from app.namings import admin, librarian, director, bibliographer

router = Router()

register_role = {
    admin: [],
    librarian: [],
    director: [],
    bibliographer: [],
}


@router.message(CommandStart())
async def cmd_start(message):
    await message.answer('Добро пожаловать в библиотеку ада! Выберите роль', reply_markup=kb.mainButtons)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await CategoriesRepository.getCategories()


@router.message(F.text.in_([admin, librarian, director, bibliographer]))
async def choose_role(message: Message):
    register_role[message.text].append(message.from_user.id)
    print(f"{message.text}: ", register_role[message.text])
    await message.answer("Выберите, с чем вы хотите работать", reply_markup=kb.first_part_tables)


@router.message(F.text == "Еще -->")
async def choose_entities_more(message: Message):
    await message.reply("Выберите, с чем вы хотите работать", reply_markup=kb.second_part_tables)


@router.message(F.text == "<-- Назад")
async def choose_entities_back(message: Message):
    await message.reply("Выберите, с чем вы хотите работать", reply_markup=kb.first_part_tables)


def delete_register_role(value):
    keys = {k for k, v in register_role.items() if value in v}

    for key in keys:
        register_role[key].remove(value)


@router.message(F.text == "Выход")
async def exit_button(message: Message):
    delete_register_role(message.from_user.id)
    await message.reply("Выход", reply_markup=kb.mainButtons)


@router.callback_query(F.data == "back")
async def back_button(call: CallbackQuery):
    await call.message.answer("Выберите, с чем вы хотите работать", reply_markup=kb.first_part_tables)


async def CRUD_button(message: Message, df: pd.DataFrame, table_name: str):

    if df.empty:
        await message.reply("<b>Таблица пустая ⚠️</b>", parse_mode="HTML")
    else:
        await message.reply(text=f"<pre>{df.to_markdown()}</pre>", parse_mode="HTML")
    await message.answer("Выберите вариант", reply_markup=kb.create_inline_keyboard(table_name))

    msg = await message.answer("_", reply_markup=ReplyKeyboardRemove())
    await msg.delete()

