from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.training_analytics_data_event import TrainingAnalyticsDataEvent
    from ..models.training_analytics_data_order import TrainingAnalyticsDataOrder


T = TypeVar("T", bound="TrainingAnalyticsData")


@attr.s(auto_attribs=True)
class TrainingAnalyticsData:
    """
    Attributes:
        orders (Union[Unset, List['TrainingAnalyticsDataOrder']]):
        events (Union[Unset, List['TrainingAnalyticsDataEvent']]):
    """

    orders: Union[Unset, List["TrainingAnalyticsDataOrder"]] = UNSET
    events: Union[Unset, List["TrainingAnalyticsDataEvent"]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        orders: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.orders, Unset):
            orders = []
            for orders_item_data in self.orders:
                orders_item = orders_item_data.to_dict()

                orders.append(orders_item)

        events: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.events, Unset):
            events = []
            for events_item_data in self.events:
                events_item = events_item_data.to_dict()

                events.append(events_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if orders is not UNSET:
            field_dict["orders"] = orders
        if events is not UNSET:
            field_dict["events"] = events

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.training_analytics_data_event import TrainingAnalyticsDataEvent
        from ..models.training_analytics_data_order import TrainingAnalyticsDataOrder

        d = src_dict.copy()
        orders = []
        _orders = d.pop("orders", UNSET)
        for orders_item_data in _orders or []:
            orders_item = TrainingAnalyticsDataOrder.from_dict(orders_item_data)

            orders.append(orders_item)

        events = []
        _events = d.pop("events", UNSET)
        for events_item_data in _events or []:
            events_item = TrainingAnalyticsDataEvent.from_dict(events_item_data)

            events.append(events_item)

        training_analytics_data = cls(
            orders=orders,
            events=events,
        )

        training_analytics_data.additional_properties = d
        return training_analytics_data

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
