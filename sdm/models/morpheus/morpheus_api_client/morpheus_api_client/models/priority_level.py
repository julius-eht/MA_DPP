from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PriorityLevel")


@attr.s(auto_attribs=True)
class PriorityLevel:
    """
    Attributes:
        id (Union[Unset, str]):
        priority_level_number (Union[Unset, int]):
        time_to_deliver_in_sec (Union[Unset, float]):
        delivery_type (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    priority_level_number: Union[Unset, int] = UNSET
    time_to_deliver_in_sec: Union[Unset, float] = UNSET
    delivery_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        priority_level_number = self.priority_level_number
        time_to_deliver_in_sec = self.time_to_deliver_in_sec
        delivery_type = self.delivery_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if priority_level_number is not UNSET:
            field_dict["priorityLevelNumber"] = priority_level_number
        if time_to_deliver_in_sec is not UNSET:
            field_dict["timeToDeliverInSec"] = time_to_deliver_in_sec
        if delivery_type is not UNSET:
            field_dict["deliveryType"] = delivery_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        priority_level_number = d.pop("priorityLevelNumber", UNSET)

        time_to_deliver_in_sec = d.pop("timeToDeliverInSec", UNSET)

        delivery_type = d.pop("deliveryType", UNSET)

        priority_level = cls(
            id=id,
            priority_level_number=priority_level_number,
            time_to_deliver_in_sec=time_to_deliver_in_sec,
            delivery_type=delivery_type,
        )

        priority_level.additional_properties = d
        return priority_level

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
