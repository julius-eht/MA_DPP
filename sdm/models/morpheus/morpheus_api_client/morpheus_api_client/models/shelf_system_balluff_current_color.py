from enum import Enum


class ShelfSystemBalluffCurrentColor(str, Enum):
    BLUE = "blue"
    GREEN = "green"
    OFF = "off"
    ORANGE = "orange"
    RED = "red"
    WBK = "wbk"
    WHITE = "white"
    YELLOW = "yellow"

    def __str__(self) -> str:
        return str(self.value)
