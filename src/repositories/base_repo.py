from abc import ABC, abstractmethod


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
    def update_one(self, *args, **kwargs):
        """Обновить 1 объект в БД"""
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

    def create_one(self, *args, **kwargs):
        """Создать 1 объект в БД"""
        ...

    def retrieve_one(self, id, *args, **kwargs):
        """Вернуть 1 объект из БД"""
        ...

    def retrieve_all(self, *args, **kwargs):
        """Вернуть все объекты из БД"""
        ...

    def update_one(self, *args, **kwargs):
        """Обновить 1 объект в БД"""
        ...

    def delete_one(self, *args, **kwargs):
        """Удалить 1 объект из БД"""
        ...

    def delete_by_ids(self, *args, **kwargs):
        """Удалить несколько объектов из БД"""
        ...
