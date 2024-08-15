from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.editable_manual_instructions import EditableManualInstructions


T = TypeVar("T", bound="EditableManual")


@attr.s(auto_attribs=True)
class EditableManual:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        instructions (Union[Unset, EditableManualInstructions]):
        training_id (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    instructions: Union[Unset, "EditableManualInstructions"] = UNSET
    training_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        instructions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.instructions, Unset):
            instructions = self.instructions.to_dict()

        training_id = self.training_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if training_id is not UNSET:
            field_dict["trainingId"] = training_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.editable_manual_instructions import EditableManualInstructions

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _instructions = d.pop("instructions", UNSET)
        instructions: Union[Unset, EditableManualInstructions]
        if isinstance(_instructions, Unset):
            instructions = UNSET
        else:
            instructions = EditableManualInstructions.from_dict(_instructions)

        training_id = d.pop("trainingId", UNSET)

        editable_manual = cls(
            id=id,
            name=name,
            instructions=instructions,
            training_id=training_id,
        )

        editable_manual.additional_properties = d
        return editable_manual

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
