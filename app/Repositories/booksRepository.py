from app.Repositories.baseRepository import BaseRepository


class BooksRepository:

    @staticmethod
    async def getBooks():
        return await BaseRepository.get_query("SELECT * FROM books")

    @staticmethod
    async def getWrittenOffBooks():
        return await BaseRepository.get_query("CALL written_off_books()")
