from enum import Enum


class ValueStreamKpiConfigLayoutType(str, Enum):
    S_SHAPE = "S_SHAPE"
    U_SHAPE = "U_SHAPE"

    def __str__(self) -> str:
        return str(self.value)
