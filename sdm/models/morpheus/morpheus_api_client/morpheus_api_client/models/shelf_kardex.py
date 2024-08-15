from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ShelfKardex")


@attr.s(auto_attribs=True)
class ShelfKardex:
    """
    Attributes:
        id (Union[Unset, str]):
        shelf_system_id (Union[Unset, str]):
        part_id (Union[Unset, str]):
        shelf_id (Union[Unset, str]):
        shelf_level (Union[Unset, int]):
        start_px (Union[Unset, int]):
        end_px (Union[Unset, int]):
    """

    id: Union[Unset, str] = UNSET
    shelf_system_id: Union[Unset, str] = UNSET
    part_id: Union[Unset, str] = UNSET
    shelf_id: Union[Unset, str] = UNSET
    shelf_level: Union[Unset, int] = UNSET
    start_px: Union[Unset, int] = UNSET
    end_px: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        shelf_system_id = self.shelf_system_id
        part_id = self.part_id
        shelf_id = self.shelf_id
        shelf_level = self.shelf_level
        start_px = self.start_px
        end_px = self.end_px

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if shelf_system_id is not UNSET:
            field_dict["shelfSystemId"] = shelf_system_id
        if part_id is not UNSET:
            field_dict["partId"] = part_id
        if shelf_id is not UNSET:
            field_dict["shelfId"] = shelf_id
        if shelf_level is not UNSET:
            field_dict["shelfLevel"] = shelf_level
        if start_px is not UNSET:
            field_dict["startPx"] = start_px
        if end_px is not UNSET:
            field_dict["endPx"] = end_px

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        shelf_system_id = d.pop("shelfSystemId", UNSET)

        part_id = d.pop("partId", UNSET)

        shelf_id = d.pop("shelfId", UNSET)

        shelf_level = d.pop("shelfLevel", UNSET)

        start_px = d.pop("startPx", UNSET)

        end_px = d.pop("endPx", UNSET)

        shelf_kardex = cls(
            id=id,
            shelf_system_id=shelf_system_id,
            part_id=part_id,
            shelf_id=shelf_id,
            shelf_level=shelf_level,
            start_px=start_px,
            end_px=end_px,
        )

        shelf_kardex.additional_properties = d
        return shelf_kardex

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
