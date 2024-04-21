from abc import ABC, abstractmethod

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

from db.database import Conn

class AbstractRepo(ABC):
    """Абстрактный репозиторий"""

    @abstractmethod
    def create_one(self, *args, **kwargs):
        """Создать 1 объект в БД"""
        raise NotImplementedError

    @abstractmethod
    def retrieve_one(self, *args, **kwargs):
        """Вернуть 1 объект из БД"""
        raise NotImplementedError

    @abstractmethod
    def retrieve_all(self, *args, **kwargs):
        """Вернуть все объекты из БД"""
        raise NotImplementedError

    @abstractmethod
    def delete_one(self, *args, **kwargs):
        """Удалить 1 объект из БД"""
        raise NotImplementedError

    @abstractmethod
    def delete_by_ids(self, *args, **kwargs):
        """Удалить несколько объектов из БД"""
        raise NotImplementedError


class BaseRepo(AbstractRepo):
    """Базовый репозиторий"""
    table_name: str | None = None
    db = Conn()

    async def create_one(self, data):
        """Создать 1 объект в БД"""
        columns = ', '.join(data.key())
        placeholders = ', '.join(data.value())
        query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
        try:
            self.conn = await self.db.connect_to_db()
            await self.conn.execute(query)
            print(f"Запрос выполнен.")
        except Exception as e:
            print(f"Ошибка: {e}")
        
    async def retrieve_one(self, id):
        """Вернуть 1 объект из БД"""
        query = f"SELECT * FROM {self.table_name} WHERE id = {id}"
        try:
            self.conn = await self.db.connect_to_db()
            await self.conn.execute(query)
            print(f"Запрос выполнен.")
        except Exception as e:
            print(f"Ошибка: {e}")
            
    async def retrieve_all(self):
        """Вернуть все объекты из БД"""
        query = f"SELECT * FROM {self.table_name}"
        try:
            self.conn = await self.db.connect_to_db()
            await self.conn.execute(query)
            print(f"Запрос выполнен.")
        except Exception as e:
            print(f"Ошибка: {e}")
       
    async def delete_one(self, id):
        """Удалить 1 объект из БД"""
        query = f"DELETE FROM {self.table_name} WHERE id = {id}"
        try:
            self.conn = await self.db.connect_to_db()
            await self.conn.execute(query)
            print(f"Запрос выполнен.")
        except Exception as e:
            print(f"Ошибка: {e}")
            

    async def delete_by_ids(self, ids: tuple[int, ...]):
        """Удалить несколько объектов из БД"""
        ids = ', '.join(ids)
        query = f"DELETE FROM {self.table_name} WHERE id IN {ids}"
        try:
            self.conn = await self.db.connect_to_db()
            answer = await self.conn.execute(query)
            print(f"Запрос выполнен. {answer}")
        except Exception as e:
            print(f"Ошибка: {e}")
