from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EditablePartType")


@attr.s(auto_attribs=True)
class EditablePartType:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        picking_mode_id (Union[Unset, str]):
        training_id (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    picking_mode_id: Union[Unset, str] = UNSET
    training_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        picking_mode_id = self.picking_mode_id
        training_id = self.training_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if picking_mode_id is not UNSET:
            field_dict["pickingModeId"] = picking_mode_id
        if training_id is not UNSET:
            field_dict["trainingId"] = training_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        picking_mode_id = d.pop("pickingModeId", UNSET)

        training_id = d.pop("trainingId", UNSET)

        editable_part_type = cls(
            id=id,
            name=name,
            picking_mode_id=picking_mode_id,
            training_id=training_id,
        )

        editable_part_type.additional_properties = d
        return editable_part_type

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
