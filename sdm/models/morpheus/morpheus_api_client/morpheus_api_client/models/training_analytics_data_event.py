import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TrainingAnalyticsDataEvent")


@attr.s(auto_attribs=True)
class TrainingAnalyticsDataEvent:
    """
    Attributes:
        time_enter (Union[Unset, datetime.datetime]):
        time_leave (Union[Unset, datetime.datetime]):
        pol_id (Union[Unset, str]):
        order_id (Union[Unset, str]):
    """

    time_enter: Union[Unset, datetime.datetime] = UNSET
    time_leave: Union[Unset, datetime.datetime] = UNSET
    pol_id: Union[Unset, str] = UNSET
    order_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        time_enter: Union[Unset, str] = UNSET
        if not isinstance(self.time_enter, Unset):
            time_enter = self.time_enter.isoformat()

        time_leave: Union[Unset, str] = UNSET
        if not isinstance(self.time_leave, Unset):
            time_leave = self.time_leave.isoformat()

        pol_id = self.pol_id
        order_id = self.order_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if time_enter is not UNSET:
            field_dict["timeEnter"] = time_enter
        if time_leave is not UNSET:
            field_dict["timeLeave"] = time_leave
        if pol_id is not UNSET:
            field_dict["polId"] = pol_id
        if order_id is not UNSET:
            field_dict["orderId"] = order_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _time_enter = d.pop("timeEnter", UNSET)
        time_enter: Union[Unset, datetime.datetime]
        if isinstance(_time_enter, Unset):
            time_enter = UNSET
        else:
            time_enter = isoparse(_time_enter)

        _time_leave = d.pop("timeLeave", UNSET)
        time_leave: Union[Unset, datetime.datetime]
        if isinstance(_time_leave, Unset):
            time_leave = UNSET
        else:
            time_leave = isoparse(_time_leave)

        pol_id = d.pop("polId", UNSET)

        order_id = d.pop("orderId", UNSET)

        training_analytics_data_event = cls(
            time_enter=time_enter,
            time_leave=time_leave,
            pol_id=pol_id,
            order_id=order_id,
        )

        training_analytics_data_event.additional_properties = d
        return training_analytics_data_event

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
