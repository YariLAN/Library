from app.Repositories.baseRepository import BaseRepository


class LibrariansRepository:

    @staticmethod
    async def getLibrarians():
        return await BaseRepository.get_query("SELECT * FROM ibrarians")


    @staticmethod
    async def getLibrarian(id):
        return await BaseRepository.get_query(f"SELECT * FROM ibrarians WHERE id = {id}")

    @staticmethod
    async def getLibrarianByName(lastName, firstName, patronymic):
        return await BaseRepository.get_query(
            f"SELECT * FROM ibrarians "
            f"WHERE "
                f"last_name = '{lastName}' "
                f"AND first_name = '{firstName}' "
                f"AND patronymic = '{patronymic}'")