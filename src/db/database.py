import asyncio
import asyncpg

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import settings

class Conn():       
    async def connect_to_db(self):
        try:
            self.conn = await asyncpg.connect(
                user=settings.DB_USER,
                password=settings.DB_PASS,
                database=settings.DB_NAME,
                host=settings.DB_HOST
            )
            print(f"Подключен")
            return self.conn
        except Exception as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            return False

    async def create_tables(self):
        try:
            await self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT PRIMARY KEY UNIQUE
                );
                CREATE TABLE IF NOT EXISTS users_packs (
                    user_id INT REFERENCES users(user_id),
                    link VARCHAR(512)
                );
                CREATE TABLE IF NOT EXISTS pic_templates(
                    id SERIAL PRIMARY KEY UNIQUE,
                    url VARCHAR(512) UNIQUE
                );
            ''')
            print("Таблицы успешно создана!")
        except Exception as e:
            print(f"Ошибка при создании таблицы: {e}")

