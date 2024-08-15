import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProcessData")


@attr.s(auto_attribs=True)
class ProcessData:
    """
    Attributes:
        id (Union[Unset, str]):
        entry_time (Union[Unset, datetime.datetime]):
        output_time (Union[Unset, datetime.datetime]):
        work_station_id (Union[Unset, str]):
        work_process_id (Union[Unset, str]):
        engine_status (Union[Unset, bool]):
        at_entry_point (Union[Unset, bool]):
        pole_housing_id (Union[Unset, str]):
        game_round_id (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    entry_time: Union[Unset, datetime.datetime] = UNSET
    output_time: Union[Unset, datetime.datetime] = UNSET
    work_station_id: Union[Unset, str] = UNSET
    work_process_id: Union[Unset, str] = UNSET
    engine_status: Union[Unset, bool] = UNSET
    at_entry_point: Union[Unset, bool] = UNSET
    pole_housing_id: Union[Unset, str] = UNSET
    game_round_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        entry_time: Union[Unset, str] = UNSET
        if not isinstance(self.entry_time, Unset):
            entry_time = self.entry_time.isoformat()

        output_time: Union[Unset, str] = UNSET
        if not isinstance(self.output_time, Unset):
            output_time = self.output_time.isoformat()

        work_station_id = self.work_station_id
        work_process_id = self.work_process_id
        engine_status = self.engine_status
        at_entry_point = self.at_entry_point
        pole_housing_id = self.pole_housing_id
        game_round_id = self.game_round_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if entry_time is not UNSET:
            field_dict["entryTime"] = entry_time
        if output_time is not UNSET:
            field_dict["outputTime"] = output_time
        if work_station_id is not UNSET:
            field_dict["workStationId"] = work_station_id
        if work_process_id is not UNSET:
            field_dict["workProcessId"] = work_process_id
        if engine_status is not UNSET:
            field_dict["engineStatus"] = engine_status
        if at_entry_point is not UNSET:
            field_dict["atEntryPoint"] = at_entry_point
        if pole_housing_id is not UNSET:
            field_dict["poleHousingId"] = pole_housing_id
        if game_round_id is not UNSET:
            field_dict["gameRoundId"] = game_round_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _entry_time = d.pop("entryTime", UNSET)
        entry_time: Union[Unset, datetime.datetime]
        if isinstance(_entry_time, Unset):
            entry_time = UNSET
        else:
            entry_time = isoparse(_entry_time)

        _output_time = d.pop("outputTime", UNSET)
        output_time: Union[Unset, datetime.datetime]
        if isinstance(_output_time, Unset):
            output_time = UNSET
        else:
            output_time = isoparse(_output_time)

        work_station_id = d.pop("workStationId", UNSET)

        work_process_id = d.pop("workProcessId", UNSET)

        engine_status = d.pop("engineStatus", UNSET)

        at_entry_point = d.pop("atEntryPoint", UNSET)

        pole_housing_id = d.pop("poleHousingId", UNSET)

        game_round_id = d.pop("gameRoundId", UNSET)

        process_data = cls(
            id=id,
            entry_time=entry_time,
            output_time=output_time,
            work_station_id=work_station_id,
            work_process_id=work_process_id,
            engine_status=engine_status,
            at_entry_point=at_entry_point,
            pole_housing_id=pole_housing_id,
            game_round_id=game_round_id,
        )

        process_data.additional_properties = d
        return process_data

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
