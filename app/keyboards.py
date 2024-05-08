from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

mainButtons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Администратор БД 👌")],
    [KeyboardButton(text="Директор Библиотеки")],
    [KeyboardButton(text="Библиотекарь"), KeyboardButton(text="Библиограф")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню...")

librarian = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Принятые от читателей книги")],
    [KeyboardButton(text="Сданные книги")],
    [KeyboardButton(text="Читатели")]],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню...")


# Кнопки для выбора из категорий
async def set_inline_buttons_from_db(entities):
    buttons = []
    for item in entities:
        buttons.append(InlineKeyboardButton(text=item.name, callback_data=item.id))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


async def create_reply_keyboard(entity):
    keyboard = ReplyKeyboardBuilder()

    for action in ["Добавить", "Удалить", "Изменить", "Показать"]:
        keyboard.add(KeyboardButton(text=f"{action} {entity}"))
    keyboard.add(KeyboardButton(text="Список всех"))
    keyboard.add(KeyboardButton(text="Выход"))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)

readers = create_reply_keyboard("читателя")
books = create_reply_keyboard("книгу")
issueds = create_reply_keyboard("сданную книгу")