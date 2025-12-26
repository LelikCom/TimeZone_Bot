from aiogram import Bot, Dispatcher
from bot.config import Config
from bot.services.database import Database

# Создаём экземпляры
bot = Bot(token=Config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()
db = Database()

# Запускаем подключение к базе и автосоздание таблиц
async def on_startup():
    await db.connect()
    await db.create_tables()
