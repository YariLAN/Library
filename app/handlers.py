from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import F, Router

import app.keyboards as kb
from app.Repositories.categoriesRepository import categoriesRepository

router = Router()


@router.message(CommandStart())
async def cmd_start(message):
    await message.answer('Добро пожаловать в библиотеку ада! Выберите роль', reply_markup=kb.mainButtons)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await categoriesRepository.getCategories()


# Плохой пример
@router.message(F.text == "Библиотекарь")
async def getAlex(message: Message):
    await message.answer("Выберите функции библиотекаря", reply_markup=kb.librarian)


@router.message(F.text == "Читатели")
async def getReaders(message: Message):
    # Получаем список читателей из база данных

    await message.answer("Выберите вариант", reply_markup=await kb.readers)

