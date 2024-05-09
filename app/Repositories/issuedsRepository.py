from app.Repositories.baseRepository import BaseRepository


class IssuedsRepository:

    @staticmethod
    async def getIssueds():
        return await BaseRepository.get_query("SELECT * FROM issued")
