import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="KeyPerformanceIndicator")


@attr.s(auto_attribs=True)
class KeyPerformanceIndicator:
    """
    Attributes:
        id (Union[Unset, str]):
        affiliation_id (Union[Unset, str]):
        start_time_game_round (Union[Unset, datetime.datetime]):
        end_time_game_round (Union[Unset, datetime.datetime]):
        end_time_training (Union[Unset, datetime.datetime]):
        start_time_calculation (Union[Unset, datetime.datetime]):
        number_ok_parts (Union[Unset, int]):
        number_not_ok_parts (Union[Unset, int]):
        oee (Union[Unset, float]):
        quality (Union[Unset, float]):
        availability (Union[Unset, float]):
        power (Union[Unset, float]):
        average_cycle_time (Union[Unset, float]):
    """

    id: Union[Unset, str] = UNSET
    affiliation_id: Union[Unset, str] = UNSET
    start_time_game_round: Union[Unset, datetime.datetime] = UNSET
    end_time_game_round: Union[Unset, datetime.datetime] = UNSET
    end_time_training: Union[Unset, datetime.datetime] = UNSET
    start_time_calculation: Union[Unset, datetime.datetime] = UNSET
    number_ok_parts: Union[Unset, int] = UNSET
    number_not_ok_parts: Union[Unset, int] = UNSET
    oee: Union[Unset, float] = UNSET
    quality: Union[Unset, float] = UNSET
    availability: Union[Unset, float] = UNSET
    power: Union[Unset, float] = UNSET
    average_cycle_time: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        affiliation_id = self.affiliation_id
        start_time_game_round: Union[Unset, str] = UNSET
        if not isinstance(self.start_time_game_round, Unset):
            start_time_game_round = self.start_time_game_round.isoformat()

        end_time_game_round: Union[Unset, str] = UNSET
        if not isinstance(self.end_time_game_round, Unset):
            end_time_game_round = self.end_time_game_round.isoformat()

        end_time_training: Union[Unset, str] = UNSET
        if not isinstance(self.end_time_training, Unset):
            end_time_training = self.end_time_training.isoformat()

        start_time_calculation: Union[Unset, str] = UNSET
        if not isinstance(self.start_time_calculation, Unset):
            start_time_calculation = self.start_time_calculation.isoformat()

        number_ok_parts = self.number_ok_parts
        number_not_ok_parts = self.number_not_ok_parts
        oee = self.oee
        quality = self.quality
        availability = self.availability
        power = self.power
        average_cycle_time = self.average_cycle_time

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if affiliation_id is not UNSET:
            field_dict["affiliationId"] = affiliation_id
        if start_time_game_round is not UNSET:
            field_dict["startTimeGameRound"] = start_time_game_round
        if end_time_game_round is not UNSET:
            field_dict["endTimeGameRound"] = end_time_game_round
        if end_time_training is not UNSET:
            field_dict["endTimeTraining"] = end_time_training
        if start_time_calculation is not UNSET:
            field_dict["startTimeCalculation"] = start_time_calculation
        if number_ok_parts is not UNSET:
            field_dict["numberOkParts"] = number_ok_parts
        if number_not_ok_parts is not UNSET:
            field_dict["numberNotOkParts"] = number_not_ok_parts
        if oee is not UNSET:
            field_dict["oee"] = oee
        if quality is not UNSET:
            field_dict["quality"] = quality
        if availability is not UNSET:
            field_dict["availability"] = availability
        if power is not UNSET:
            field_dict["power"] = power
        if average_cycle_time is not UNSET:
            field_dict["averageCycleTime"] = average_cycle_time

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        affiliation_id = d.pop("affiliationId", UNSET)

        _start_time_game_round = d.pop("startTimeGameRound", UNSET)
        start_time_game_round: Union[Unset, datetime.datetime]
        if isinstance(_start_time_game_round, Unset):
            start_time_game_round = UNSET
        else:
            start_time_game_round = isoparse(_start_time_game_round)

        _end_time_game_round = d.pop("endTimeGameRound", UNSET)
        end_time_game_round: Union[Unset, datetime.datetime]
        if isinstance(_end_time_game_round, Unset):
            end_time_game_round = UNSET
        else:
            end_time_game_round = isoparse(_end_time_game_round)

        _end_time_training = d.pop("endTimeTraining", UNSET)
        end_time_training: Union[Unset, datetime.datetime]
        if isinstance(_end_time_training, Unset):
            end_time_training = UNSET
        else:
            end_time_training = isoparse(_end_time_training)

        _start_time_calculation = d.pop("startTimeCalculation", UNSET)
        start_time_calculation: Union[Unset, datetime.datetime]
        if isinstance(_start_time_calculation, Unset):
            start_time_calculation = UNSET
        else:
            start_time_calculation = isoparse(_start_time_calculation)

        number_ok_parts = d.pop("numberOkParts", UNSET)

        number_not_ok_parts = d.pop("numberNotOkParts", UNSET)

        oee = d.pop("oee", UNSET)

        quality = d.pop("quality", UNSET)

        availability = d.pop("availability", UNSET)

        power = d.pop("power", UNSET)

        average_cycle_time = d.pop("averageCycleTime", UNSET)

        key_performance_indicator = cls(
            id=id,
            affiliation_id=affiliation_id,
            start_time_game_round=start_time_game_round,
            end_time_game_round=end_time_game_round,
            end_time_training=end_time_training,
            start_time_calculation=start_time_calculation,
            number_ok_parts=number_ok_parts,
            number_not_ok_parts=number_not_ok_parts,
            oee=oee,
            quality=quality,
            availability=availability,
            power=power,
            average_cycle_time=average_cycle_time,
        )

        key_performance_indicator.additional_properties = d
        return key_performance_indicator

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
