from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.variant_bill_of_materials import VariantBillOfMaterials


T = TypeVar("T", bound="Variant")


@attr.s(auto_attribs=True)
class Variant:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        bill_of_materials (Union[Unset, VariantBillOfMaterials]):
        work_process_sequence_ids (Union[Unset, List[str]]):
        current_work_process_id (Union[Unset, str]):
        editable (Union[Unset, bool]):
        copy (Union[Unset, bool]):
        pole_housing_length (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    bill_of_materials: Union[Unset, "VariantBillOfMaterials"] = UNSET
    work_process_sequence_ids: Union[Unset, List[str]] = UNSET
    current_work_process_id: Union[Unset, str] = UNSET
    editable: Union[Unset, bool] = UNSET
    copy: Union[Unset, bool] = UNSET
    pole_housing_length: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        bill_of_materials: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.bill_of_materials, Unset):
            bill_of_materials = self.bill_of_materials.to_dict()

        work_process_sequence_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.work_process_sequence_ids, Unset):
            work_process_sequence_ids = self.work_process_sequence_ids

        current_work_process_id = self.current_work_process_id
        editable = self.editable
        copy = self.copy
        pole_housing_length = self.pole_housing_length

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if bill_of_materials is not UNSET:
            field_dict["billOfMaterials"] = bill_of_materials
        if work_process_sequence_ids is not UNSET:
            field_dict["workProcessSequenceIds"] = work_process_sequence_ids
        if current_work_process_id is not UNSET:
            field_dict["currentWorkProcessId"] = current_work_process_id
        if editable is not UNSET:
            field_dict["editable"] = editable
        if copy is not UNSET:
            field_dict["copy"] = copy
        if pole_housing_length is not UNSET:
            field_dict["poleHousingLength"] = pole_housing_length

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.variant_bill_of_materials import VariantBillOfMaterials

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        _bill_of_materials = d.pop("billOfMaterials", UNSET)
        bill_of_materials: Union[Unset, VariantBillOfMaterials]
        if isinstance(_bill_of_materials, Unset):
            bill_of_materials = UNSET
        else:
            bill_of_materials = VariantBillOfMaterials.from_dict(_bill_of_materials)

        work_process_sequence_ids = cast(List[str], d.pop("workProcessSequenceIds", UNSET))

        current_work_process_id = d.pop("currentWorkProcessId", UNSET)

        editable = d.pop("editable", UNSET)

        copy = d.pop("copy", UNSET)

        pole_housing_length = d.pop("poleHousingLength", UNSET)

        variant = cls(
            id=id,
            name=name,
            bill_of_materials=bill_of_materials,
            work_process_sequence_ids=work_process_sequence_ids,
            current_work_process_id=current_work_process_id,
            editable=editable,
            copy=copy,
            pole_housing_length=pole_housing_length,
        )

        variant.additional_properties = d
        return variant

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
