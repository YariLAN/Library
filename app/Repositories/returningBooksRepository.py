from app.Repositories.baseRepository import BaseRepository


class ReturningBooksRepository:

    @staticmethod
    async def getReturningBooks():
        return await BaseRepository.get_query("SELECT * FROM returning_books")
