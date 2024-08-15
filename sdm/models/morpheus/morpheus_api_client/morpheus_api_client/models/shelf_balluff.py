from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ShelfBalluff")


@attr.s(auto_attribs=True)
class ShelfBalluff:
    """
    Attributes:
        id (Union[Unset, str]):
        shelf_system_id (Union[Unset, str]):
        part_id (Union[Unset, str]):
        port_id (Union[Unset, int]):
    """

    id: Union[Unset, str] = UNSET
    shelf_system_id: Union[Unset, str] = UNSET
    part_id: Union[Unset, str] = UNSET
    port_id: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        shelf_system_id = self.shelf_system_id
        part_id = self.part_id
        port_id = self.port_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if shelf_system_id is not UNSET:
            field_dict["shelfSystemId"] = shelf_system_id
        if part_id is not UNSET:
            field_dict["partId"] = part_id
        if port_id is not UNSET:
            field_dict["portId"] = port_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        shelf_system_id = d.pop("shelfSystemId", UNSET)

        part_id = d.pop("partId", UNSET)

        port_id = d.pop("portId", UNSET)

        shelf_balluff = cls(
            id=id,
            shelf_system_id=shelf_system_id,
            part_id=part_id,
            port_id=port_id,
        )

        shelf_balluff.additional_properties = d
        return shelf_balluff

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
