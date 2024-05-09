from aiogram import F, Router
from aiogram.types import Message

from app.Repositories.fineRepository import FineRepository
from app.Repositories.fineRepository import FineTypesRepository

from app.handlers import CRUD_button

router = Router()


@router.message(F.text == "Штрафы")
async def get_fines(message: Message):
    df = await FineRepository.getFines()

    df.set_index("id_fine", inplace=True)

    await CRUD_button(message, df, "fines")


@router.message(F.text == "Виды штрафов")
async def get_fine_types(message: Message):
    df = await FineTypesRepository.getFinesTypes()

    df = df.rename(columns={"id_fine_type": "id", "name_fine": "name", "amount_fine": "amount"})
    df.set_index("id", inplace=True)

    await CRUD_button(message, df, "fine_type")
