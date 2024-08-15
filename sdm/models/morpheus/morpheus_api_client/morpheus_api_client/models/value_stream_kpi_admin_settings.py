from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ValueStreamKpiAdminSettings")


@attr.s(auto_attribs=True)
class ValueStreamKpiAdminSettings:
    """
    Attributes:
        id (Union[Unset, str]):
        operator_view (Union[Unset, bool]):
    """

    id: Union[Unset, str] = UNSET
    operator_view: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        operator_view = self.operator_view

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if operator_view is not UNSET:
            field_dict["operatorView"] = operator_view

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        operator_view = d.pop("operatorView", UNSET)

        value_stream_kpi_admin_settings = cls(
            id=id,
            operator_view=operator_view,
        )

        value_stream_kpi_admin_settings.additional_properties = d
        return value_stream_kpi_admin_settings

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
