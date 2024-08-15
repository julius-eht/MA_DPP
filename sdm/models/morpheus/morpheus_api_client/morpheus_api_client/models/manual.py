from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.manual_instructions import ManualInstructions


T = TypeVar("T", bound="Manual")


@attr.s(auto_attribs=True)
class Manual:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        instructions (Union[Unset, ManualInstructions]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    instructions: Union[Unset, "ManualInstructions"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        instructions: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.instructions, Unset):
            instructions = self.instructions.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if instructions is not UNSET:
            field_dict["instructions"] = instructions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.manual_instructions import ManualInstructions

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _instructions = d.pop("instructions", UNSET)
        instructions: Union[Unset, ManualInstructions]
        if isinstance(_instructions, Unset):
            instructions = UNSET
        else:
            instructions = ManualInstructions.from_dict(_instructions)

        manual = cls(
            id=id,
            name=name,
            instructions=instructions,
        )

        manual.additional_properties = d
        return manual

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
