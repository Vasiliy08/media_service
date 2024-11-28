from dataclasses import dataclass

from src.exceptions.base import ApplicationException


@dataclass
class FileNotFoundException(ApplicationException):
    uuid: str

    @property
    def message(self):
        return f"Файл c uuid {self.uuid} не найден"
