from enum import Enum


class WebhookEventsItem(str, Enum):
    FINISHED_PRODUCTION_PROCESS = "FINISHED_PRODUCTION_PROCESS"
    POLE_HOUSING_ENTERED_PRODUCTION = "POLE_HOUSING_ENTERED_PRODUCTION"
    POLE_HOUSING_FINISHED_PRODUCTION = "POLE_HOUSING_FINISHED_PRODUCTION"
    POLE_HOUSING_MATCHED_TO_ORDER = "POLE_HOUSING_MATCHED_TO_ORDER"
    START_GAME_ROUND = "START_GAME_ROUND"
    START_TRAINING = "START_TRAINING"

    def __str__(self) -> str:
        return str(self.value)
