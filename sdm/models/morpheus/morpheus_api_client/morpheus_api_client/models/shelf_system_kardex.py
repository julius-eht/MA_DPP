from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ShelfSystemKardex")


@attr.s(auto_attribs=True)
class ShelfSystemKardex:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        active (Union[Unset, bool]):
        ip_adress (Union[Unset, str]):
        port (Union[Unset, str]):
        relative_url (Union[Unset, str]):
        megamat_id (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    ip_adress: Union[Unset, str] = UNSET
    port: Union[Unset, str] = UNSET
    relative_url: Union[Unset, str] = UNSET
    megamat_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        active = self.active
        ip_adress = self.ip_adress
        port = self.port
        relative_url = self.relative_url
        megamat_id = self.megamat_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if active is not UNSET:
            field_dict["active"] = active
        if ip_adress is not UNSET:
            field_dict["ipAdress"] = ip_adress
        if port is not UNSET:
            field_dict["port"] = port
        if relative_url is not UNSET:
            field_dict["relativeUrl"] = relative_url
        if megamat_id is not UNSET:
            field_dict["megamatId"] = megamat_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        active = d.pop("active", UNSET)

        ip_adress = d.pop("ipAdress", UNSET)

        port = d.pop("port", UNSET)

        relative_url = d.pop("relativeUrl", UNSET)

        megamat_id = d.pop("megamatId", UNSET)

        shelf_system_kardex = cls(
            id=id,
            name=name,
            active=active,
            ip_adress=ip_adress,
            port=port,
            relative_url=relative_url,
            megamat_id=megamat_id,
        )

        shelf_system_kardex.additional_properties = d
        return shelf_system_kardex

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
