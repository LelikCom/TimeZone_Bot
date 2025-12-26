class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        import asyncpg
        from bot.config import Config
        self.pool = await asyncpg.create_pool(dsn=Config.DATABASE_URL)

    async def create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            full_name TEXT,
            is_authorized BOOLEAN DEFAULT FALSE
        );
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query)

    # ✅ ПРОВЕРКА авторизации пользователя
    async def is_user_authorized(self, user_id: int) -> bool:
        query = "SELECT is_authorized FROM users WHERE user_id = $1;"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, user_id)
            return row and row["is_authorized"]

    # ✅ Авторизация пользователя
    async def authorize_user(self, user_id: int):
        query = """
        INSERT INTO users (user_id, is_authorized)
        VALUES ($1, TRUE)
        ON CONFLICT (user_id) DO UPDATE SET is_authorized = TRUE;
        """
        async with self.pool.acquire() as conn:
            await conn.execute(query, user_id)
