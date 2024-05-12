import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, \
    KeyboardButton
from aiogram import F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
import tabulate

from app.DbModels.Reader import ReaderMapper, Reader
from app.Repositories.categoriesRepository import CategoriesRepository

import app.keyboards as kb
import app.StatesModels.Reader.createReaderState as dto
from app.Repositories.discountRepository import DiscountRepository
from app.Repositories.readersRepository import ReadersRepository
from app.handlers import CRUD_button_with_table

router = Router()

# InlineKeyboardMarkup
crud_reader_inline = kb.create_inline_keyboard(Reader.__tableName__)


@router.callback_query(F.data.startswith("reader"))
async def CRUD_reader(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "reader_add":
        await state.set_state(dto.CreateReaderDto.name)
        await callback_query.message.answer("Введите ФИО читателя", reply_markup=kb.cancel_keyboard)

    if callback_query.data == "reader_list":
        await getReaders(callback_query.message)


async def inline_categories():
    df = await CategoriesRepository.getCategories()
    data = df.values.tolist()

    builder = InlineKeyboardBuilder()
    for row in data:
        builder.add(InlineKeyboardButton(text=row[1], callback_data=f"{row[0]}"))

    builder.adjust(2)

    return builder.as_markup()


# Добавление читателя
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
    await message.answer("Введите email читателя (при наличие)", reply_markup=kb.warning_email_button)


@router.message(dto.CreateReaderDto.email)
async def addReader_email(message: Message, state: FSMContext):
    email = None if message.text == kb.warning_email_button.keyboard[0][0].text else message.text

    await state.update_data(email=email)

    data = await state.get_data()
    result = await ReadersRepository.add_reader(
        ReaderMapper.toMap(data["name"], data["category"], data["address"], data["phone"], data["email"]))

    if result:
        await message.answer(f"Читатель с ФИО {data['name']} успешно добавлен", reply_markup=crud_reader_inline)
    else:
        await message.answer("Доавить не удалось", reply_markup=crud_reader_inline)


@router.message(F.text == "Читатели")
async def getReaders(message: Message):
    df = await getReadersDataframe()

    await CRUD_button_with_table(message, df, "reader")


async def getReadersDataframe():
    df = await ReadersRepository.getReaders()

    df = df.rename(columns={"fk_id_category": "c", "id_reader": "id", "first_name": "name"})
    df.set_index('id', inplace=True)

    return df


@router.message(F.text == "Категории читателей")
async def getCategories(message: Message):
    df = await CategoriesRepository.getCategories()
    await CRUD_button_with_table(message, df, "category_type")


@router.message(F.text == "Скидки")
async def getDiscounts(message: Message):
    df = await DiscountRepository.getDiscounts()
    df = df.rename(columns={"id_discount": "id", "amount_discount": "amount"})
    df.set_index('id', inplace=True)

    await CRUD_button_with_table(message, df, "discount_type")
