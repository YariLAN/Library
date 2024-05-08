import asyncio
from aiogram import Bot, Dispatcher, F

import app.handlers as main_handlers
import app.Handlers.readers_handlers as readers_handlers


async def main():
    bot = Bot(token='6352754030:AAGDI-kcK-6iLZwPlFFuQgVLJmQj_kpMEDQ')
    # Управляет хэндлерами

    dp = Dispatcher()
    dp.include_router(main_handlers.router)
    dp.include_router(readers_handlers.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
