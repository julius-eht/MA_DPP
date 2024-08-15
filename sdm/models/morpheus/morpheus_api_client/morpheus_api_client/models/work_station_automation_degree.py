from enum import Enum


class WorkStationAutomationDegree(str, Enum):
    AUTOMATED = "AUTOMATED"
    MANUAL = "MANUAL"
    PARTLY_AUTOMATED = "PARTLY_AUTOMATED"

    def __str__(self) -> str:
        return str(self.value)
