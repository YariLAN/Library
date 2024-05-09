import pandas as pd
import pymysql

from app.DatabaseProvider import provider


class BaseRepository:
    @staticmethod
    async def get_query(sql: str):
        try:
            connect = provider.connection
            with connect.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()

                return pd.DataFrame(result)
        except Exception as e:
            print("Ошибка при получении. Запрос: ", sql, "\nОшибка:", e)
            return None