import asyncio
from aiogram import Bot, Dispatcher

import app.handlers as main_handlers
import app.Handlers.readers_handlers as readers_handlers
import app.Handlers.books_handlers as books_handlers
import app.Handlers.librarians_handlers as librarians_handlers
import app.Handlers.bookNotLibrary_handlers as bookNotLibrary_handlers
import app.Handlers.fines_handlers as fines_handlers
import app.Handlers.genre_handlers as genre_handlers
import app.Handlers.stored_procedures_handlers as stored_procedures

from app.token import token


async def main():
    bot = Bot(token=token)
    # Управляет хэндлерами

    dp = Dispatcher()

    dp.include_router(main_handlers.router)
    dp.include_routers(
        readers_handlers.router,
        books_handlers.router,
        bookNotLibrary_handlers.router,
        librarians_handlers.router,
        fines_handlers.router,
        genre_handlers.router,
        stored_procedures.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
