import app.DatabaseProvider.provider as provider
import pandas as pd

from app.DbModels.Reader import Reader


class ReadersRepository(object):

    @staticmethod
    async def add_reader(reader: Reader):
        connect = provider.connection

        try:
            with connect.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO {reader.__tableName__} VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)",
                    (reader.lastName, reader.firstName, reader.patronymic, reader.category_id,
                     reader.address, reader.phone, reader.email))

                connect.commit()

                return True
        except Exception as e:
            print("Ошибка при добавлении читателя", e)
            return False
