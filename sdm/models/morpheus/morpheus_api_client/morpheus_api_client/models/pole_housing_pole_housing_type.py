from enum import Enum


class PoleHousingPoleHousingType(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"

    def __str__(self) -> str:
        return str(self.value)
