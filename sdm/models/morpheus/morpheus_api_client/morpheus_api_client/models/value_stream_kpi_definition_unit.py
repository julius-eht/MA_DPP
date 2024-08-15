from enum import Enum


class ValueStreamKpiDefinitionUnit(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    SECOND = "SECOND"

    def __str__(self) -> str:
        return str(self.value)
