from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.editable_variant_bill_of_materials import EditableVariantBillOfMaterials


T = TypeVar("T", bound="EditableVariant")


@attr.s(auto_attribs=True)
class EditableVariant:
    """
    Attributes:
        id (Union[Unset, str]):
        original_id (Union[Unset, str]):
        name (Union[Unset, str]):
        bill_of_materials (Union[Unset, EditableVariantBillOfMaterials]):
        work_process_sequence_ids (Union[Unset, List[str]]):
        editable (Union[Unset, bool]):
        active_training_id (Union[Unset, str]):
        displayed (Union[Unset, bool]):
        pole_housing_length (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    original_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    bill_of_materials: Union[Unset, "EditableVariantBillOfMaterials"] = UNSET
    work_process_sequence_ids: Union[Unset, List[str]] = UNSET
    editable: Union[Unset, bool] = UNSET
    active_training_id: Union[Unset, str] = UNSET
    displayed: Union[Unset, bool] = UNSET
    pole_housing_length: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        original_id = self.original_id
        name = self.name
        bill_of_materials: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bill_of_materials, Unset):
            bill_of_materials = self.bill_of_materials.to_dict()

        work_process_sequence_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.work_process_sequence_ids, Unset):
            work_process_sequence_ids = self.work_process_sequence_ids

        editable = self.editable
        active_training_id = self.active_training_id
        displayed = self.displayed
        pole_housing_length = self.pole_housing_length

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if original_id is not UNSET:
            field_dict["originalId"] = original_id
        if name is not UNSET:
            field_dict["name"] = name
        if bill_of_materials is not UNSET:
            field_dict["billOfMaterials"] = bill_of_materials
        if work_process_sequence_ids is not UNSET:
            field_dict["workProcessSequenceIds"] = work_process_sequence_ids
        if editable is not UNSET:
            field_dict["editable"] = editable
        if active_training_id is not UNSET:
            field_dict["activeTrainingId"] = active_training_id
        if displayed is not UNSET:
            field_dict["displayed"] = displayed
        if pole_housing_length is not UNSET:
            field_dict["poleHousingLength"] = pole_housing_length

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.editable_variant_bill_of_materials import EditableVariantBillOfMaterials

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        original_id = d.pop("originalId", UNSET)

        name = d.pop("name", UNSET)

        _bill_of_materials = d.pop("billOfMaterials", UNSET)
        bill_of_materials: Union[Unset, EditableVariantBillOfMaterials]
        if isinstance(_bill_of_materials, Unset):
            bill_of_materials = UNSET
        else:
            bill_of_materials = EditableVariantBillOfMaterials.from_dict(_bill_of_materials)

        work_process_sequence_ids = cast(List[str], d.pop("workProcessSequenceIds", UNSET))

        editable = d.pop("editable", UNSET)

        active_training_id = d.pop("activeTrainingId", UNSET)

        displayed = d.pop("displayed", UNSET)

        pole_housing_length = d.pop("poleHousingLength", UNSET)

        editable_variant = cls(
            id=id,
            original_id=original_id,
            name=name,
            bill_of_materials=bill_of_materials,
            work_process_sequence_ids=work_process_sequence_ids,
            editable=editable,
            active_training_id=active_training_id,
            displayed=displayed,
            pole_housing_length=pole_housing_length,
        )

        editable_variant.additional_properties = d
        return editable_variant

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
