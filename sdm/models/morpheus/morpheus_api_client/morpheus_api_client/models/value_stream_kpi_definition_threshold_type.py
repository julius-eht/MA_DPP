from enum import Enum


class ValueStreamKpiDefinitionThresholdType(str, Enum):
    BIGGER_IS_BETTER = "BIGGER_IS_BETTER"
    SMALLER_IS_BETTER = "SMALLER_IS_BETTER"

    def __str__(self) -> str:
        return str(self.value)
