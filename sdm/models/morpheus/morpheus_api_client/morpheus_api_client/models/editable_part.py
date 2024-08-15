from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditablePart")


@attr.s(auto_attribs=True)
class EditablePart:
    """
    Attributes:
        id (Union[Unset, str]):
        original_id (Union[Unset, str]):
        part_type_id (Union[Unset, str]):
        name (Union[Unset, str]):
        number (Union[Unset, str]):
        active_shelf_id (Union[Unset, str]):
        photo (Union[Unset, str]):
        active_training_id (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    original_id: Union[Unset, str] = UNSET
    part_type_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    number: Union[Unset, str] = UNSET
    active_shelf_id: Union[Unset, str] = UNSET
    photo: Union[Unset, str] = UNSET
    active_training_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        original_id = self.original_id
        part_type_id = self.part_type_id
        name = self.name
        number = self.number
        active_shelf_id = self.active_shelf_id
        photo = self.photo
        active_training_id = self.active_training_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if original_id is not UNSET:
            field_dict["originalId"] = original_id
        if part_type_id is not UNSET:
            field_dict["partTypeId"] = part_type_id
        if name is not UNSET:
            field_dict["name"] = name
        if number is not UNSET:
            field_dict["number"] = number
        if active_shelf_id is not UNSET:
            field_dict["activeShelfId"] = active_shelf_id
        if photo is not UNSET:
            field_dict["photo"] = photo
        if active_training_id is not UNSET:
            field_dict["activeTrainingId"] = active_training_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        original_id = d.pop("originalId", UNSET)

        part_type_id = d.pop("partTypeId", UNSET)

        name = d.pop("name", UNSET)

        number = d.pop("number", UNSET)

        active_shelf_id = d.pop("activeShelfId", UNSET)

        photo = d.pop("photo", UNSET)

        active_training_id = d.pop("activeTrainingId", UNSET)

        editable_part = cls(
            id=id,
            original_id=original_id,
            part_type_id=part_type_id,
            name=name,
            number=number,
            active_shelf_id=active_shelf_id,
            photo=photo,
            active_training_id=active_training_id,
        )

        editable_part.additional_properties = d
        return editable_part

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
