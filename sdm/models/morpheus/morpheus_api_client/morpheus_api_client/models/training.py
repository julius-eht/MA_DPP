import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="Training")


@attr.s(auto_attribs=True)
class Training:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        start_time (Union[Unset, datetime.datetime]):
        end_time (Union[Unset, datetime.datetime]):
        game_round_ids (Union[Unset, List[str]]):
        pole_housing_ids (Union[Unset, List[str]]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    game_round_ids: Union[Unset, List[str]] = UNSET
    pole_housing_ids: Union[Unset, List[str]] = UNSET
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

        game_round_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.game_round_ids, Unset):
            game_round_ids = self.game_round_ids

        pole_housing_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.pole_housing_ids, Unset):
            pole_housing_ids = self.pole_housing_ids

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
        if game_round_ids is not UNSET:
            field_dict["gameRoundIds"] = game_round_ids
        if pole_housing_ids is not UNSET:
            field_dict["poleHousingIds"] = pole_housing_ids

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

        game_round_ids = cast(List[str], d.pop("gameRoundIds", UNSET))

        pole_housing_ids = cast(List[str], d.pop("poleHousingIds", UNSET))

        training = cls(
            id=id,
            name=name,
            start_time=start_time,
            end_time=end_time,
            game_round_ids=game_round_ids,
            pole_housing_ids=pole_housing_ids,
        )

        training.additional_properties = d
        return training

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
