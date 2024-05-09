from app.Repositories.baseRepository import BaseRepository


class LibrariansRepository:

    @staticmethod
    async def getLibrarians():
        return await BaseRepository.get_query("SELECT * FROM ibrarians")
