from app.Repositories.baseRepository import BaseRepository


class FineRepository:

    @staticmethod
    async def getFines():
        return await BaseRepository.get_query("SELECT * FROM fines")


class FineTypesRepository:

    @staticmethod
    async def getFinesTypes():
        return await BaseRepository.get_query("SELECT * FROM fine_type")