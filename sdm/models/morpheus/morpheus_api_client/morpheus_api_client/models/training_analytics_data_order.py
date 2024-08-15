import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TrainingAnalyticsDataOrder")


@attr.s(auto_attribs=True)
class TrainingAnalyticsDataOrder:
    """
    Attributes:
        start_time (Union[Unset, datetime.datetime]):
        finish_time (Union[Unset, datetime.datetime]):
        variant (Union[Unset, str]):
        pol_id (Union[Unset, List[str]]):
        amount (Union[Unset, int]):
    """

    start_time: Union[Unset, datetime.datetime] = UNSET
    finish_time: Union[Unset, datetime.datetime] = UNSET
    variant: Union[Unset, str] = UNSET
    pol_id: Union[Unset, List[str]] = UNSET
    amount: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        finish_time: Union[Unset, str] = UNSET
        if not isinstance(self.finish_time, Unset):
            finish_time = self.finish_time.isoformat()

        variant = self.variant
        pol_id: Union[Unset, List[str]] = UNSET
        if not isinstance(self.pol_id, Unset):
            pol_id = self.pol_id

        amount = self.amount

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if finish_time is not UNSET:
            field_dict["finishTime"] = finish_time
        if variant is not UNSET:
            field_dict["variant"] = variant
        if pol_id is not UNSET:
            field_dict["polId"] = pol_id
        if amount is not UNSET:
            field_dict["amount"] = amount

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _start_time = d.pop("startTime", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        _finish_time = d.pop("finishTime", UNSET)
        finish_time: Union[Unset, datetime.datetime]
        if isinstance(_finish_time, Unset):
            finish_time = UNSET
        else:
            finish_time = isoparse(_finish_time)

        variant = d.pop("variant", UNSET)

        pol_id = cast(List[str], d.pop("polId", UNSET))

        amount = d.pop("amount", UNSET)

        training_analytics_data_order = cls(
            start_time=start_time,
            finish_time=finish_time,
            variant=variant,
            pol_id=pol_id,
            amount=amount,
        )

        training_analytics_data_order.additional_properties = d
        return training_analytics_data_order

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
