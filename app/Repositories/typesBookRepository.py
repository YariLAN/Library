from app.Repositories.baseRepository import BaseRepository


class GenreRepository:

    @staticmethod
    async def getGenre():
        return await BaseRepository.get_query("SELECT * FROM genre")


class TypesLiteratureRepository:

    @staticmethod
    async def getGenre():
        return await BaseRepository.get_query("SELECT * FROM literature_type")
