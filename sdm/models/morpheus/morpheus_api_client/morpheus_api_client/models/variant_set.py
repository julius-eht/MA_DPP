from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.variant_set_parts import VariantSetParts


T = TypeVar("T", bound="VariantSet")


@attr.s(auto_attribs=True)
class VariantSet:
    """
    Attributes:
        variants (Union[Unset, List[str]]):
        parts (Union[Unset, VariantSetParts]):
        description (Union[Unset, str]):
        warning (Union[Unset, str]):
        photos (Union[Unset, List[str]]):
    """

    variants: Union[Unset, List[str]] = UNSET
    parts: Union[Unset, "VariantSetParts"] = UNSET
    description: Union[Unset, str] = UNSET
    warning: Union[Unset, str] = UNSET
    photos: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        variants: Union[Unset, List[str]] = UNSET
        if not isinstance(self.variants, Unset):
            variants = self.variants

        parts: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.parts, Unset):
            parts = self.parts.to_dict()

        description = self.description
        warning = self.warning
        photos: Union[Unset, List[str]] = UNSET
        if not isinstance(self.photos, Unset):
            photos = self.photos

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if variants is not UNSET:
            field_dict["variants"] = variants
        if parts is not UNSET:
            field_dict["parts"] = parts
        if description is not UNSET:
            field_dict["description"] = description
        if warning is not UNSET:
            field_dict["warning"] = warning
        if photos is not UNSET:
            field_dict["photos"] = photos

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.variant_set_parts import VariantSetParts

        d = src_dict.copy()
        variants = cast(List[str], d.pop("variants", UNSET))

        _parts = d.pop("parts", UNSET)
        parts: Union[Unset, VariantSetParts]
        if isinstance(_parts, Unset):
            parts = UNSET
        else:
            parts = VariantSetParts.from_dict(_parts)

        description = d.pop("description", UNSET)

        warning = d.pop("warning", UNSET)

        photos = cast(List[str], d.pop("photos", UNSET))

        variant_set = cls(
            variants=variants,
            parts=parts,
            description=description,
            warning=warning,
            photos=photos,
        )

        variant_set.additional_properties = d
        return variant_set

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
