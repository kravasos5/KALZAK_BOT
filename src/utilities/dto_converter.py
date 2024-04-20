from abc import ABC, abstractmethod


class AbstractDTOConverter(ABC):
    """Абстрактный конвертер DTO"""

    @staticmethod
    @abstractmethod
    def from_raw_to_dto(*args, **kwargs):
        """Конвертировать ответ БД в DTO"""
        raise NotImplementedError


class DTOConverter(AbstractDTOConverter):
    """Конвертер DTO"""

    @staticmethod
    def from_raw_to_dto(*args, **kwargs):
        """Конвертировать ответ БД в DTO"""
        ...
