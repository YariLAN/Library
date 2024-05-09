import app.DatabaseProvider.provider as provider
import pandas as pd

from app.Repositories.baseRepository import BaseRepository


class CategoriesRepository:

    @staticmethod
    async def getCategories():
        return await BaseRepository.get_query("SELECT * FROM category_type")

    async def getCategory(id: int):
        return await BaseRepository.get_query(f"SELECT * FROM category_type WHERE id_category= {id}")
