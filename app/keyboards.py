from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.DbModels.Reader import Reader
from app.namings import admin, librarian, director, bibliographer, d_action

mainButtons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=admin)],
    [KeyboardButton(text=director)],
    [KeyboardButton(text=librarian), KeyboardButton(text=bibliographer)]],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню...")

first_part_tables_buttons = [
    [KeyboardButton(text="Библиотекари"), KeyboardButton(text="Книги"), KeyboardButton(text="Читатели")],
    [KeyboardButton(text="Сданные книги"), KeyboardButton(text="Принятые от читателей книги"),
     KeyboardButton(text="Категории читателей")],
    [KeyboardButton(text="Жанры книг"), KeyboardButton(text="Жанры литературы")],
    [KeyboardButton(text="Выход"), KeyboardButton(text="Еще -->")]]

second_part_tables_buttons = [
    [KeyboardButton(text="Виды штрафов")],
    [KeyboardButton(text="Штрафы")],
    [KeyboardButton(text="Скидки")],
    [KeyboardButton(text="<-- Назад")]
]

first_part_tables = ReplyKeyboardMarkup(keyboard=first_part_tables_buttons,
                                        resize_keyboard=True,
                                        input_field_placeholder="Выберите пункт меню...")

second_part_tables = ReplyKeyboardMarkup(keyboard=second_part_tables_buttons,
                                         resize_keyboard=True,
                                         input_field_placeholder="Выберите пункт меню...")

warning_email_button = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Почты нет")]], resize_keyboard=True)

cancel_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отменить")]], resize_keyboard=True)


# Кнопки для выбора из категорий
async def set_inline_buttons_from_db(entities):
    buttons = []
    for item in entities:
        buttons.append(InlineKeyboardButton(text=item.name, callback_data=item.id))
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def create_reply_keyboard(entity):
    keyboard = ReplyKeyboardBuilder()

    for action in ["Добавить", "Удалить", "Изменить", "Показать"]:
        keyboard.add(KeyboardButton(text=f"{action} {entity}", callback_data=action))
    keyboard.add(KeyboardButton(text="Список всех"))
    keyboard.add(KeyboardButton(text="Вернуться к другим данным"))
    return keyboard.adjust(2).as_markup(resize_keyboard=True)


def create_inline_keyboard(table_name: str):
    keyboard = InlineKeyboardBuilder()

    for key in d_action.keys():
        keyboard.add(InlineKeyboardButton(text=key, callback_data=f"{table_name}_{d_action[key]}"))

    keyboard.add(InlineKeyboardButton(text="Вернуться к другим данным", callback_data="back"))

    return keyboard.adjust(2).as_markup()


def create_keyboard():
    keyboard = ReplyKeyboardBuilder()

    keyboard.add(KeyboardButton(text="Вернуться к другим данным"))

    return keyboard.as_markup(resize_keyboard=True)


back_button = create_keyboard()
