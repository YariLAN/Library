from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram import F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.DbModels.Reader import ReaderMapper
from app.Repositories.categoriesRepository import categoriesRepository

import app.keyboards as kb
import app.StatesModels.Reader.createReaderDto as dto
from app.Repositories.readersRepository import ReadersRepository

router = Router()


@router.message(F.text == "Добавить читателя")
async def addReader(message: Message, state: FSMContext):
    await state.set_state(dto.CreateReaderDto.name)
    await message.answer("Введите ФИО читателя")


async def inline_categories():
    df = await categoriesRepository.getCategories()
    data = df.values.tolist()

    builder = InlineKeyboardBuilder()
    for row in data:
        builder.add(InlineKeyboardButton(text=row[1], callback_data=f"{row[0]}"))

    builder.adjust(2)

    return builder.as_markup()


@router.message(dto.CreateReaderDto.name)
async def addReader_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(dto.CreateReaderDto.category)
    await message.answer("Выберите категорию читателя", reply_markup=await inline_categories())


@router.callback_query(dto.CreateReaderDto.category)
async def addReader_category(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback_query.data)
    await state.set_state(dto.CreateReaderDto.address)
    await callback_query.message.answer("Введите адрес читателя")


@router.message(dto.CreateReaderDto.address)
async def addReader_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(dto.CreateReaderDto.phone)
    await message.answer("Введите телефон читателя (8 800 555 35 35)")


@router.message(dto.CreateReaderDto.phone)
async def addReader_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(dto.CreateReaderDto.email)
    await message.answer("Введите email читателя (при наличие)",
                         keyboard=ReplyKeyboardMarkup(
                             keyboard=[[KeyboardButton(text="Почты нет")]]))


@router.message(dto.CreateReaderDto.email)
async def addReader_email(message: Message, state: FSMContext):
    email = None if message.text == "Почты нет" else message.text

    await state.update_data(email=email)

    data = await state.get_data()
    result = await ReadersRepository.add_reader(
        ReaderMapper.toMap(data["name"], data["category"], data["address"], data["phone"], data["email"]))

    if result:
        await message.answer(f"Читатель с ФИО {data['name']} успешно добавлен",
                             reply_markup=await kb.readers)
