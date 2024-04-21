from base_repo import BaseRepo

class PicTemplatesRepo(BaseRepo):
    table_name = 'pic_templates'
    col_1 = 'url'

    async def create_one(self, url:str):
        """Создать 1 объект в БД"""
        query = f"INSERT INTO {self.table_name} ({self.col_1}) VALUES ($1)"
        try:
            self.conn = await self.db.connect_to_db()
            await self.conn.execute(query, url)
            print(f"Запрос выполнен.")
        except Exception as e:
            print(f"Ошибка: {e}")
