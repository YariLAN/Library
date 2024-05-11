from aiogram import Router, F
from aiogram.filters import state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
from app.Handlers.readers_handlers import inline_categories
from app.Repositories.readersRepository import ReadersRepository
from app.StatesModels.Category.getCategoryDto import GetCategoryDto
from app.namings import d_ent_func

router = Router()


async def init_additional_buttons(message: Message):
    await message.answer("Выберите сущность для работы с дополнительными функциями",
                         reply_markup=kb.additional_buttons)


@router.message(F.text == "Дополнительные функции")
async def create_additional_functions_keyboard(message: Message):
    await message.delete()
    await init_additional_buttons(message)


@router.message(F.text == d_ent_func[0])
async def create_func_readers_keyboard(message: Message):
    await message.delete()
    await message.answer("Список функций", reply_markup=kb.additional_readers_buttons)


@router.message(F.text == "Назад")
async def go_back(message: Message):
    await init_additional_buttons(message)


@router.message(F.text == "Читатели по категории")
async def get_readers_by_category(message: Message, state: FSMContext):
    await state.set_state(GetCategoryDto.name)
    await message.answer("Выберите категорию читателя", reply_markup=await inline_categories())


@router.callback_query(GetCategoryDto.name)
async def get_readers_by_category_name(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(name=callback_query.data)

    data = await state.get_data()
    df = await ReadersRepository.getReadersByCategory(int(data["name"]))

    df = df.rename(columns={"fk_id_category": "c", "id_reader": "id", "first_name": "name"})
    df.set_index('id', inplace=True)

    await callback_query.message.reply(text=f"<pre>{df.to_markdown()}</pre>", parse_mode="HTML")
