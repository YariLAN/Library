from app.Repositories.baseRepository import BaseRepository


class GenreRepository:

    @staticmethod
    async def getGenre():
        return await BaseRepository.get_query("SELECT * FROM genre")

    @staticmethod
    async def getPopularGenres(start_date: str, end_date: str):
        return await BaseRepository.get_query(f"CALL popular_genre('{start_date}', '{end_date}');")


class TypesLiteratureRepository:

    @staticmethod
    async def getGenre():
        return await BaseRepository.get_query("SELECT * FROM literature_type")
