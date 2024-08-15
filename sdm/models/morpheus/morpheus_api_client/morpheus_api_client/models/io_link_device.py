from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.io_linkidentification import IoLinkidentification


T = TypeVar("T", bound="IoLinkDevice")


@attr.s(auto_attribs=True)
class IoLinkDevice:
    """
    Attributes:
        id (Union[Unset, str]):
        io_link_device_variant_id (Union[Unset, str]):
        io_link_identification (Union[Unset, IoLinkidentification]):
    """

    id: Union[Unset, str] = UNSET
    io_link_device_variant_id: Union[Unset, str] = UNSET
    io_link_identification: Union[Unset, "IoLinkidentification"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        io_link_device_variant_id = self.io_link_device_variant_id
        io_link_identification: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.io_link_identification, Unset):
            io_link_identification = self.io_link_identification.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if io_link_device_variant_id is not UNSET:
            field_dict["ioLinkDeviceVariantId"] = io_link_device_variant_id
        if io_link_identification is not UNSET:
            field_dict["ioLinkIdentification"] = io_link_identification

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.io_linkidentification import IoLinkidentification

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        io_link_device_variant_id = d.pop("ioLinkDeviceVariantId", UNSET)

        _io_link_identification = d.pop("ioLinkIdentification", UNSET)
        io_link_identification: Union[Unset, IoLinkidentification]
        if isinstance(_io_link_identification, Unset):
            io_link_identification = UNSET
        else:
            io_link_identification = IoLinkidentification.from_dict(_io_link_identification)

        io_link_device = cls(
            id=id,
            io_link_device_variant_id=io_link_device_variant_id,
            io_link_identification=io_link_identification,
        )

        io_link_device.additional_properties = d
        return io_link_device

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
