from enum import Enum


class OrderOrderState(str, Enum):
    ARCHIVED = "ARCHIVED"
    DELIVERED = "DELIVERED"
    IN_PROGRESS = "IN_PROGRESS"
    ORDERED = "ORDERED"

    def __str__(self) -> str:
        return str(self.value)
