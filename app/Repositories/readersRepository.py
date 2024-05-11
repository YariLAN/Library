import app.DatabaseProvider.provider as provider
import pandas as pd

from app.DbModels.Reader import Reader
from app.Repositories.baseRepository import BaseRepository


class ReadersRepository(object):

    @staticmethod
    async def getReaders():
        return await BaseRepository.get_query("SELECT * FROM reader")

    @staticmethod
    async def getReadersByCategory(category: int):
        return await BaseRepository.get_query(f"CALL get_readers_by_category({category})")

    @staticmethod
    async def getReadersByBook(book_id: int):
        return await BaseRepository.get_query(f"CALL get_reader_by_book({book_id})")

    @staticmethod
    async def getReadersByGenreOfBookInPeriod(genre: str, start_date: str, end_date: str):
        return await BaseRepository.get_query(f"CALL get_readers_with_books_in_period({start_date}, {end_date}, {genre})")

    @staticmethod
    async def getReadersWithOverdue():
        return await BaseRepository.get_query("CALL get_readers_with_overdue()")

    @staticmethod
    async def getTotalCost(id_reader: int, date_last: str):
        return await BaseRepository.get_query(f"CALL total_cost({id_reader}, {date_last})")

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
