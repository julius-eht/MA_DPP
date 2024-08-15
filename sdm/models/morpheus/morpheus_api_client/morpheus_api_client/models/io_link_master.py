from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.io_link_master_connected_iolink_devices import IoLinkMasterConnectedIolinkDevices


T = TypeVar("T", bound="IoLinkMaster")


@attr.s(auto_attribs=True)
class IoLinkMaster:
    """
    Attributes:
        id (Union[Unset, str]):
        connected_iolink_devices (Union[Unset, IoLinkMasterConnectedIolinkDevices]):
    """

    id: Union[Unset, str] = UNSET
    connected_iolink_devices: Union[Unset, "IoLinkMasterConnectedIolinkDevices"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        connected_iolink_devices: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.connected_iolink_devices, Unset):
            connected_iolink_devices = self.connected_iolink_devices.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if connected_iolink_devices is not UNSET:
            field_dict["connectedIolinkDevices"] = connected_iolink_devices

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.io_link_master_connected_iolink_devices import IoLinkMasterConnectedIolinkDevices

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _connected_iolink_devices = d.pop("connectedIolinkDevices", UNSET)
        connected_iolink_devices: Union[Unset, IoLinkMasterConnectedIolinkDevices]
        if isinstance(_connected_iolink_devices, Unset):
            connected_iolink_devices = UNSET
        else:
            connected_iolink_devices = IoLinkMasterConnectedIolinkDevices.from_dict(_connected_iolink_devices)

        io_link_master = cls(
            id=id,
            connected_iolink_devices=connected_iolink_devices,
        )

        io_link_master.additional_properties = d
        return io_link_master

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
