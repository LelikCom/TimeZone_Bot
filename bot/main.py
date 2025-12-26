import asyncio
from bot.loader import bot, dp, on_startup
from bot.handlers import user

async def main():
    await on_startup()
    dp.include_router(user.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
