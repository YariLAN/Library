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

    @staticmethod
    async def getLibrariansWork(start_date: str, end_date: str):
        return await BaseRepository.get_query(f"CALL get_librarians_work('{start_date}', '{end_date}')")

    @staticmethod
    async def getExperience(experience: int):
        return await BaseRepository.get_query(f"CALL get_experience({experience})")

    @staticmethod
    async def getCountCategory(id_librarian: int):
        return await BaseRepository.get_query(f"CALL get_count_category({id_librarian})")
