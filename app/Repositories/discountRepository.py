from app.Repositories.baseRepository import BaseRepository


class DiscountRepository:

    @staticmethod
    async def getDiscounts():
        return await BaseRepository.get_query("SELECT * FROM discount_type")