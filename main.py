import asyncio
from aiogram import Bot, Dispatcher, F

from app.handlers import router
from app.Handlers.readers_handlers import router


async def main():
    bot = Bot(token='6352754030:AAFp7g_YlEpnIY8deOF1m7-8tibQVGLtA5w')
    # Управляет хэндлерами

    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
