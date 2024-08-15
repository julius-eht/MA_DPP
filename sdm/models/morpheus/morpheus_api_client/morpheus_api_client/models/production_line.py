from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProductionLine")


@attr.s(auto_attribs=True)
class ProductionLine:
    """
    Attributes:
        id (Union[Unset, str]):
        work_station_ids (Union[Unset, List[str]]):
        work_station_id_order_penetration_point (Union[Unset, str]):
        work_station_id_pole_housing_entry_point (Union[Unset, str]):
        name (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    work_station_ids: Union[Unset, List[str]] = UNSET
    work_station_id_order_penetration_point: Union[Unset, str] = UNSET
    work_station_id_pole_housing_entry_point: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        work_station_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.work_station_ids, Unset):
            work_station_ids = self.work_station_ids

        work_station_id_order_penetration_point = self.work_station_id_order_penetration_point
        work_station_id_pole_housing_entry_point = self.work_station_id_pole_housing_entry_point
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if work_station_ids is not UNSET:
            field_dict["workStationIds"] = work_station_ids
        if work_station_id_order_penetration_point is not UNSET:
            field_dict["workStationIdOrderPenetrationPoint"] = work_station_id_order_penetration_point
        if work_station_id_pole_housing_entry_point is not UNSET:
            field_dict["workStationIdPoleHousingEntryPoint"] = work_station_id_pole_housing_entry_point
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        work_station_ids = cast(List[str], d.pop("workStationIds", UNSET))

        work_station_id_order_penetration_point = d.pop("workStationIdOrderPenetrationPoint", UNSET)

        work_station_id_pole_housing_entry_point = d.pop("workStationIdPoleHousingEntryPoint", UNSET)

        name = d.pop("name", UNSET)

        production_line = cls(
            id=id,
            work_station_ids=work_station_ids,
            work_station_id_order_penetration_point=work_station_id_order_penetration_point,
            work_station_id_pole_housing_entry_point=work_station_id_pole_housing_entry_point,
            name=name,
        )

        production_line.additional_properties = d
        return production_line

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
