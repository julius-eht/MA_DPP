from enum import Enum


class IoLinkDeviceVariantDeviceType(str, Enum):
    ACTUATOR = "ACTUATOR"
    PICK_BY_LIGHT = "PICK_BY_LIGHT"
    RFID = "RFID"
    SENSOR = "SENSOR"
    STATUS_LIGHT = "STATUS_LIGHT"

    def __str__(self) -> str:
        return str(self.value)
