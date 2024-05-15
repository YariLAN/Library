from app.DbModels.ReturningBook import ReturningBook
from app.Repositories.baseRepository import BaseRepository


class ReturningBooksRepository:

    @staticmethod
    async def getReturningBooks():
        return await BaseRepository.get_query("SELECT * FROM returning_books")

    @staticmethod
    async def createReturningBooks(rb: ReturningBook):
        return await BaseRepository.add_query(
            f"INSERT INTO {rb.__tableName__} VALUES (NULL, {rb.librarian_id}, {rb.issued_book_id}, '{rb.date_of_actual}')")
