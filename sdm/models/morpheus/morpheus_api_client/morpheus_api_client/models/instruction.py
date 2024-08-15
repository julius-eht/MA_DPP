from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.variant_set import VariantSet


T = TypeVar("T", bound="Instruction")


@attr.s(auto_attribs=True)
class Instruction:
    """
    Attributes:
        video_id (Union[Unset, str]):
        variant_sets (Union[Unset, List['VariantSet']]):
    """

    video_id: Union[Unset, str] = UNSET
    variant_sets: Union[Unset, List["VariantSet"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        video_id = self.video_id
        variant_sets: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.variant_sets, Unset):
            variant_sets = []
            for variant_sets_item_data in self.variant_sets:
                variant_sets_item = variant_sets_item_data.to_dict()

                variant_sets.append(variant_sets_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if video_id is not UNSET:
            field_dict["video_id"] = video_id
        if variant_sets is not UNSET:
            field_dict["variant_sets"] = variant_sets

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.variant_set import VariantSet

        d = src_dict.copy()
        video_id = d.pop("video_id", UNSET)

        variant_sets = []
        _variant_sets = d.pop("variant_sets", UNSET)
        for variant_sets_item_data in _variant_sets or []:
            variant_sets_item = VariantSet.from_dict(variant_sets_item_data)

            variant_sets.append(variant_sets_item)

        instruction = cls(
            video_id=video_id,
            variant_sets=variant_sets,
        )

        instruction.additional_properties = d
        return instruction

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
