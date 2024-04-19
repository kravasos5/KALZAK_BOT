from abc import ABC, abstractmethod


class AbstractDTOConverter(ABC):
    """Абстрактный конвертер DTO"""

    @abstractmethod
    def from_raw_to_dto(self, *args, **kwargs):
        """Конвертировать ответ БД в DTO"""
        raise NotImplementedError


class DTOConverter(AbstractDTOConverter):
    """Конвертер DTO"""

    def from_raw_to_dto(self, *args, **kwargs):
        """Конвертировать ответ БД в DTO"""
        ...
