import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GameRound")


@attr.s(auto_attribs=True)
class GameRound:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        start_time (Union[Unset, datetime.datetime]):
        end_time (Union[Unset, datetime.datetime]):
        pole_housing_ids (Union[Unset, List[str]]):
        production_line_id (Union[Unset, str]):
        enable_express_order (Union[Unset, bool]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    pole_housing_ids: Union[Unset, List[str]] = UNSET
    production_line_id: Union[Unset, str] = UNSET
    enable_express_order: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        end_time: Union[Unset, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat()

        pole_housing_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.pole_housing_ids, Unset):
            pole_housing_ids = self.pole_housing_ids

        production_line_id = self.production_line_id
        enable_express_order = self.enable_express_order

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if pole_housing_ids is not UNSET:
            field_dict["poleHousingIds"] = pole_housing_ids
        if production_line_id is not UNSET:
            field_dict["productionLineId"] = production_line_id
        if enable_express_order is not UNSET:
            field_dict["enableExpressOrder"] = enable_express_order

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _start_time = d.pop("startTime", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        _end_time = d.pop("endTime", UNSET)
        end_time: Union[Unset, datetime.datetime]
        if isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        pole_housing_ids = cast(List[str], d.pop("poleHousingIds", UNSET))

        production_line_id = d.pop("productionLineId", UNSET)

        enable_express_order = d.pop("enableExpressOrder", UNSET)

        game_round = cls(
            id=id,
            name=name,
            start_time=start_time,
            end_time=end_time,
            pole_housing_ids=pole_housing_ids,
            production_line_id=production_line_id,
            enable_express_order=enable_express_order,
        )

        game_round.additional_properties = d
        return game_round

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
