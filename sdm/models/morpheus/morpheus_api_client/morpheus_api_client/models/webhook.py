from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.webhook_events_item import WebhookEventsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="Webhook")


@attr.s(auto_attribs=True)
class Webhook:
    """
    Attributes:
        id (Union[Unset, str]):
        endpoint (Union[Unset, str]):
        events (Union[Unset, List[WebhookEventsItem]]):
    """

    id: Union[Unset, str] = UNSET
    endpoint: Union[Unset, str] = UNSET
    events: Union[Unset, List[WebhookEventsItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        endpoint = self.endpoint
        events: Union[Unset, List[str]] = UNSET
        if not isinstance(self.events, Unset):
            events = []
            for events_item_data in self.events:
                events_item = events_item_data.value

                events.append(events_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if endpoint is not UNSET:
            field_dict["endpoint"] = endpoint
        if events is not UNSET:
            field_dict["events"] = events

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        endpoint = d.pop("endpoint", UNSET)

        events = []
        _events = d.pop("events", UNSET)
        for events_item_data in _events or []:
            events_item = WebhookEventsItem(events_item_data)

            events.append(events_item)

        webhook = cls(
            id=id,
            endpoint=endpoint,
            events=events,
        )

        webhook.additional_properties = d
        return webhook

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
