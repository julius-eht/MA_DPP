from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="IoLinkidentification")


@attr.s(auto_attribs=True)
class IoLinkidentification:
    """
    Attributes:
        vendor_id (Union[Unset, int]):
        device_id (Union[Unset, int]):
        port_number (Union[Unset, int]):
        vendor_name (Union[Unset, str]):
        vendor_text (Union[Unset, str]):
        product_name (Union[Unset, str]):
        product_id (Union[Unset, str]):
        product_text (Union[Unset, str]):
        hardware_revision (Union[Unset, str]):
        firmware_revision (Union[Unset, str]):
        application_specific_tag (Union[Unset, str]):
        io_link_revision (Union[Unset, str]):
    """

    vendor_id: Union[Unset, int] = UNSET
    device_id: Union[Unset, int] = UNSET
    port_number: Union[Unset, int] = UNSET
    vendor_name: Union[Unset, str] = UNSET
    vendor_text: Union[Unset, str] = UNSET
    product_name: Union[Unset, str] = UNSET
    product_id: Union[Unset, str] = UNSET
    product_text: Union[Unset, str] = UNSET
    hardware_revision: Union[Unset, str] = UNSET
    firmware_revision: Union[Unset, str] = UNSET
    application_specific_tag: Union[Unset, str] = UNSET
    io_link_revision: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        vendor_id = self.vendor_id
        device_id = self.device_id
        port_number = self.port_number
        vendor_name = self.vendor_name
        vendor_text = self.vendor_text
        product_name = self.product_name
        product_id = self.product_id
        product_text = self.product_text
        hardware_revision = self.hardware_revision
        firmware_revision = self.firmware_revision
        application_specific_tag = self.application_specific_tag
        io_link_revision = self.io_link_revision

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if vendor_id is not UNSET:
            field_dict["vendorId"] = vendor_id
        if device_id is not UNSET:
            field_dict["deviceId"] = device_id
        if port_number is not UNSET:
            field_dict["portNumber"] = port_number
        if vendor_name is not UNSET:
            field_dict["vendorName"] = vendor_name
        if vendor_text is not UNSET:
            field_dict["vendorText"] = vendor_text
        if product_name is not UNSET:
            field_dict["productName"] = product_name
        if product_id is not UNSET:
            field_dict["productId"] = product_id
        if product_text is not UNSET:
            field_dict["productText"] = product_text
        if hardware_revision is not UNSET:
            field_dict["hardwareRevision"] = hardware_revision
        if firmware_revision is not UNSET:
            field_dict["firmwareRevision"] = firmware_revision
        if application_specific_tag is not UNSET:
            field_dict["applicationSpecificTag"] = application_specific_tag
        if io_link_revision is not UNSET:
            field_dict["ioLinkRevision"] = io_link_revision

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        vendor_id = d.pop("vendorId", UNSET)

        device_id = d.pop("deviceId", UNSET)

        port_number = d.pop("portNumber", UNSET)

        vendor_name = d.pop("vendorName", UNSET)

        vendor_text = d.pop("vendorText", UNSET)

        product_name = d.pop("productName", UNSET)

        product_id = d.pop("productId", UNSET)

        product_text = d.pop("productText", UNSET)

        hardware_revision = d.pop("hardwareRevision", UNSET)

        firmware_revision = d.pop("firmwareRevision", UNSET)

        application_specific_tag = d.pop("applicationSpecificTag", UNSET)

        io_link_revision = d.pop("ioLinkRevision", UNSET)

        io_linkidentification = cls(
            vendor_id=vendor_id,
            device_id=device_id,
            port_number=port_number,
            vendor_name=vendor_name,
            vendor_text=vendor_text,
            product_name=product_name,
            product_id=product_id,
            product_text=product_text,
            hardware_revision=hardware_revision,
            firmware_revision=firmware_revision,
            application_specific_tag=application_specific_tag,
            io_link_revision=io_link_revision,
        )

        io_linkidentification.additional_properties = d
        return io_linkidentification

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
