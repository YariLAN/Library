from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram import F, Router

import app.keyboards as kb
import app.DtoModels.Reader.createReaderDto as dto

router = Router()


@router.message(F.text == "Добавить читателя")
async def addReader(message: Message, state: FSMContext):
    await state.set_state(dto.CreateReaderDto.name)
    await message.answer("Введите ФИО читателя")


# Временное решение

category_list = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1. Студент", callback_data="1")],
    [InlineKeyboardButton(text="1. Студент", callback_data="2")],
    [InlineKeyboardButton(text="3. Школьник", callback_data="3")]],
    resize_keyboard=True)


# Временное решение


@router.message(dto.CreateReaderDto.name)
async def addReader_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(dto.CreateReaderDto.category)
    await message.answer("Выберите категорию читателя", reply_keyboard=category_list)


@router.callback_query(dto.CreateReaderDto.category)
async def addReader_category(message: Message, callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data)
    await state.set_state(dto.CreateReaderDto.address)
    await message.answer("Введите адрес читателя")


@router.message(dto.CreateReaderDto.address)
async def addReader_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(dto.CreateReaderDto.phone)
    await message.answer("Введите телефон читателя")


@router.message(dto.CreateReaderDto.phone)
async def addReader_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(dto.CreateReaderDto.email)
    await message.answer("Введите email читателя (при наличие)")


@router.message(dto.CreateReaderDto.email)
async def addReader_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    data = await state.get_data()
    await message.answer(
        f"Ваше ФИО: {data['name']}\n"
        f"Категория: {data['category']}\n"
        f"Адрес: {data['address']}\n"
        f"Телефон: {data['phone']}\n"
        f"Email: {data['email']}")
