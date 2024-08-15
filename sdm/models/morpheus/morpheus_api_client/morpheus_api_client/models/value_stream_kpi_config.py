from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.value_stream_kpi_config_layout_type import ValueStreamKpiConfigLayoutType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ValueStreamKpiConfig")


@attr.s(auto_attribs=True)
class ValueStreamKpiConfig:
    """
    Attributes:
        id (Union[Unset, str]):
        config_name (Union[Unset, str]):
        value_stream_kpi_definition_ids (Union[Unset, List[str]]):
        takt_time (Union[Unset, float]):
        active (Union[Unset, bool]):
        layout_type (Union[Unset, ValueStreamKpiConfigLayoutType]):
    """

    id: Union[Unset, str] = UNSET
    config_name: Union[Unset, str] = UNSET
    value_stream_kpi_definition_ids: Union[Unset, List[str]] = UNSET
    takt_time: Union[Unset, float] = UNSET
    active: Union[Unset, bool] = UNSET
    layout_type: Union[Unset, ValueStreamKpiConfigLayoutType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        config_name = self.config_name
        value_stream_kpi_definition_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.value_stream_kpi_definition_ids, Unset):
            value_stream_kpi_definition_ids = self.value_stream_kpi_definition_ids

        takt_time = self.takt_time
        active = self.active
        layout_type: Union[Unset, str] = UNSET
        if not isinstance(self.layout_type, Unset):
            layout_type = self.layout_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if config_name is not UNSET:
            field_dict["configName"] = config_name
        if value_stream_kpi_definition_ids is not UNSET:
            field_dict["valueStreamKpiDefinitionIds"] = value_stream_kpi_definition_ids
        if takt_time is not UNSET:
            field_dict["taktTime"] = takt_time
        if active is not UNSET:
            field_dict["active"] = active
        if layout_type is not UNSET:
            field_dict["layoutType"] = layout_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        config_name = d.pop("configName", UNSET)

        value_stream_kpi_definition_ids = cast(List[str], d.pop("valueStreamKpiDefinitionIds", UNSET))

        takt_time = d.pop("taktTime", UNSET)

        active = d.pop("active", UNSET)

        _layout_type = d.pop("layoutType", UNSET)
        layout_type: Union[Unset, ValueStreamKpiConfigLayoutType]
        if isinstance(_layout_type, Unset):
            layout_type = UNSET
        else:
            layout_type = ValueStreamKpiConfigLayoutType(_layout_type)

        value_stream_kpi_config = cls(
            id=id,
            config_name=config_name,
            value_stream_kpi_definition_ids=value_stream_kpi_definition_ids,
            takt_time=takt_time,
            active=active,
            layout_type=layout_type,
        )

        value_stream_kpi_config.additional_properties = d
        return value_stream_kpi_config

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
