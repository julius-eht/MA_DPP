from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PartToPick")


@attr.s(auto_attribs=True)
class PartToPick:
    """
    Attributes:
        part_id (Union[Unset, str]):
        shelf_id (Union[Unset, str]):
        amount (Union[Unset, int]):
    """

    part_id: Union[Unset, str] = UNSET
    shelf_id: Union[Unset, str] = UNSET
    amount: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        part_id = self.part_id
        shelf_id = self.shelf_id
        amount = self.amount

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if part_id is not UNSET:
            field_dict["partId"] = part_id
        if shelf_id is not UNSET:
            field_dict["shelfId"] = shelf_id
        if amount is not UNSET:
            field_dict["amount"] = amount

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        part_id = d.pop("partId", UNSET)

        shelf_id = d.pop("shelfId", UNSET)

        amount = d.pop("amount", UNSET)

        part_to_pick = cls(
            part_id=part_id,
            shelf_id=shelf_id,
            amount=amount,
        )

        part_to_pick.additional_properties = d
        return part_to_pick

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
