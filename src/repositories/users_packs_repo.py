from base_repo import BaseRepo

class UsersPacksRepo(BaseRepo):
    table_name = 'users_packs'
    col_1 = 'user_id'
    col_2 = 'link'

    async def create_one(self, user_id:int, link:str):
        """Создать 1 объект в БД"""
        query = f"INSERT INTO {self.table_name} ({self.col_1}, {self.col_2}) VALUES ($1, $2)"
        try:
            self.conn = await self.db.connect_to_db()
            await self.conn.execute(query, user_id, link)
            print(f"Запрос выполнен.")
            return True
        except Exception as e:
            print(f"Ошибка: {e}")

    async def retrieve_all(self, user_id:int):
        """Вернуть все стикерпаки, которые принадлежат пользователю"""
        query = f"SELECT {self.col_2} FROM {self.table_name} WHERE {self.col_1} = $1"
        try:
            self.conn = await self.db.connect_to_db()
            records = await self.conn.fetch(query, user_id)
            links = [record['link'] for record in records]
            print(f"Запрос выполнен.\n{links}")
            return links
        except Exception as e:
            print(f"Ошибка: {e}")

    async def delete_one(self, user_id:int , link:str):
        """Удалить 1 стикерпак из БД"""
        query = f"DELETE FROM {self.table_name} WHERE {self.col_1} = $1 AND {self.col_2} = $2"
        try:
            self.conn = await self.db.connect_to_db()
            await self.conn.execute(query, user_id, link)
            print(f"Запрос выполнен.")
            return True
        except Exception as e:
            print(f"Ошибка: {e}")
    
    async def delete_by_ids(self, user_id):
        """Удалить все стикерпаки одного пользователя"""
        query = f"DELETE FROM {self.table_name} WHERE {self.col_1} = $1"
        try:
            self.conn = await self.db.connect_to_db()
            await self.conn.execute(query, user_id)
            print(f"Запрос выполнен.")
            return True
        except Exception as e:
            print(f"Ошибка: {e}")