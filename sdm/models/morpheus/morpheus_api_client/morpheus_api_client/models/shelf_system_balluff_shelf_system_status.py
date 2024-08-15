from enum import Enum


class ShelfSystemBalluffShelfSystemStatus(str, Enum):
    ERROR = "ERROR"
    OK = "OK"
    WARNING = "WARNING"

    def __str__(self) -> str:
        return str(self.value)
