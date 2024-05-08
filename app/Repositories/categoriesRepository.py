import app.DatabaseProvider.provider as provider
import pandas as pd


class categoriesRepository:
    @staticmethod
    async def getCategories():
        try:
            connect = provider.connection
            with connect.cursor() as cursor:
                cursor.execute("SELECT * FROM category_type")
                categories = cursor.fetchall()

                return pd.DataFrame(categories)
        except Exception as e:
            print("Ошибка при получении категорий:", e)
            return None

    @staticmethod
    async def getCategory(id: int):
        try:
            connect = provider.connection
            with connect.cursor() as cursor:
                cursor.execute(f"SELECT * FROM category_type WHERE id = {id}")
                category = cursor.fetchall()

                return pd.DataFrame(category)

        except Exception as e:
            print("Ошибка при получении категории:", e)
            return None
