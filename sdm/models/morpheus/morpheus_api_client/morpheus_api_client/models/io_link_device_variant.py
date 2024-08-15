from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.io_link_device_variant_device_type import IoLinkDeviceVariantDeviceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="IoLinkDeviceVariant")


@attr.s(auto_attribs=True)
class IoLinkDeviceVariant:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        device_id (Union[Unset, int]):
        device_type (Union[Unset, IoLinkDeviceVariantDeviceType]):
        can_read (Union[Unset, bool]):
        can_write (Union[Unset, bool]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    device_id: Union[Unset, int] = UNSET
    device_type: Union[Unset, IoLinkDeviceVariantDeviceType] = UNSET
    can_read: Union[Unset, bool] = UNSET
    can_write: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        device_id = self.device_id
        device_type: Union[Unset, str] = UNSET
        if not isinstance(self.device_type, Unset):
            device_type = self.device_type.value

        can_read = self.can_read
        can_write = self.can_write

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if device_id is not UNSET:
            field_dict["deviceId"] = device_id
        if device_type is not UNSET:
            field_dict["deviceType"] = device_type
        if can_read is not UNSET:
            field_dict["canRead"] = can_read
        if can_write is not UNSET:
            field_dict["canWrite"] = can_write

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        device_id = d.pop("deviceId", UNSET)

        _device_type = d.pop("deviceType", UNSET)
        device_type: Union[Unset, IoLinkDeviceVariantDeviceType]
        if isinstance(_device_type, Unset):
            device_type = UNSET
        else:
            device_type = IoLinkDeviceVariantDeviceType(_device_type)

        can_read = d.pop("canRead", UNSET)

        can_write = d.pop("canWrite", UNSET)

        io_link_device_variant = cls(
            id=id,
            name=name,
            device_id=device_id,
            device_type=device_type,
            can_read=can_read,
            can_write=can_write,
        )

        io_link_device_variant.additional_properties = d
        return io_link_device_variant

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
