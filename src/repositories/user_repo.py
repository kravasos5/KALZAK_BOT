from base_repo import BaseRepo
from pathlib import Path
import sys
import asyncio

sys.path.append(str(Path(__file__).resolve().parent.parent))



class UserRepo(BaseRepo):
    table_name = 'users'
    col_1 = 'user_id'

    async def create_one(self, id:int ):
        """Создать 1 объект в БД"""
        query = f"INSERT INTO {self.table_name} ({self.col_1}) VALUES ($1)"
        try:
            self.conn = await self.db.connect_to_db()
            await self.conn.execute(query, id)
            print(f"Запрос выполнен.")
        except Exception as e:
            print(f"Ошибка: {e}")