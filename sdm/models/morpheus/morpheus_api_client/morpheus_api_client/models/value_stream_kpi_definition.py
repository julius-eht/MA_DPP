from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.value_stream_kpi_definition_threshold_type import ValueStreamKpiDefinitionThresholdType
from ..models.value_stream_kpi_definition_unit import ValueStreamKpiDefinitionUnit
from ..types import UNSET, Unset

T = TypeVar("T", bound="ValueStreamKpiDefinition")


@attr.s(auto_attribs=True)
class ValueStreamKpiDefinition:
    """
    Attributes:
        id (Union[Unset, str]):
        target_value (Union[Unset, float]):
        value_stream_kpi_name (Union[Unset, str]):
        value_stream_kpi_config_id (Union[Unset, str]):
        unit (Union[Unset, ValueStreamKpiDefinitionUnit]):
        threshold_type (Union[Unset, ValueStreamKpiDefinitionThresholdType]):
        threshold_green (Union[Unset, float]):
        threshold_yellow (Union[Unset, float]):
        active (Union[Unset, bool]):
    """

    id: Union[Unset, str] = UNSET
    target_value: Union[Unset, float] = UNSET
    value_stream_kpi_name: Union[Unset, str] = UNSET
    value_stream_kpi_config_id: Union[Unset, str] = UNSET
    unit: Union[Unset, ValueStreamKpiDefinitionUnit] = UNSET
    threshold_type: Union[Unset, ValueStreamKpiDefinitionThresholdType] = UNSET
    threshold_green: Union[Unset, float] = UNSET
    threshold_yellow: Union[Unset, float] = UNSET
    active: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        target_value = self.target_value
        value_stream_kpi_name = self.value_stream_kpi_name
        value_stream_kpi_config_id = self.value_stream_kpi_config_id
        unit: Union[Unset, str] = UNSET
        if not isinstance(self.unit, Unset):
            unit = self.unit.value

        threshold_type: Union[Unset, str] = UNSET
        if not isinstance(self.threshold_type, Unset):
            threshold_type = self.threshold_type.value

        threshold_green = self.threshold_green
        threshold_yellow = self.threshold_yellow
        active = self.active

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if target_value is not UNSET:
            field_dict["targetValue"] = target_value
        if value_stream_kpi_name is not UNSET:
            field_dict["valueStreamKpiName"] = value_stream_kpi_name
        if value_stream_kpi_config_id is not UNSET:
            field_dict["valueStreamKpiConfigId"] = value_stream_kpi_config_id
        if unit is not UNSET:
            field_dict["unit"] = unit
        if threshold_type is not UNSET:
            field_dict["thresholdType"] = threshold_type
        if threshold_green is not UNSET:
            field_dict["thresholdGreen"] = threshold_green
        if threshold_yellow is not UNSET:
            field_dict["thresholdYellow"] = threshold_yellow
        if active is not UNSET:
            field_dict["active"] = active

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        target_value = d.pop("targetValue", UNSET)

        value_stream_kpi_name = d.pop("valueStreamKpiName", UNSET)

        value_stream_kpi_config_id = d.pop("valueStreamKpiConfigId", UNSET)

        _unit = d.pop("unit", UNSET)
        unit: Union[Unset, ValueStreamKpiDefinitionUnit]
        if isinstance(_unit, Unset):
            unit = UNSET
        else:
            unit = ValueStreamKpiDefinitionUnit(_unit)

        _threshold_type = d.pop("thresholdType", UNSET)
        threshold_type: Union[Unset, ValueStreamKpiDefinitionThresholdType]
        if isinstance(_threshold_type, Unset):
            threshold_type = UNSET
        else:
            threshold_type = ValueStreamKpiDefinitionThresholdType(_threshold_type)

        threshold_green = d.pop("thresholdGreen", UNSET)

        threshold_yellow = d.pop("thresholdYellow", UNSET)

        active = d.pop("active", UNSET)

        value_stream_kpi_definition = cls(
            id=id,
            target_value=target_value,
            value_stream_kpi_name=value_stream_kpi_name,
            value_stream_kpi_config_id=value_stream_kpi_config_id,
            unit=unit,
            threshold_type=threshold_type,
            threshold_green=threshold_green,
            threshold_yellow=threshold_yellow,
            active=active,
        )

        value_stream_kpi_definition.additional_properties = d
        return value_stream_kpi_definition

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
