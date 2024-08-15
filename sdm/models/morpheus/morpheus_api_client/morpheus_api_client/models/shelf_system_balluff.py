from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.shelf_system_balluff_current_color import ShelfSystemBalluffCurrentColor
from ..models.shelf_system_balluff_shelf_system_status import ShelfSystemBalluffShelfSystemStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="ShelfSystemBalluff")


@attr.s(auto_attribs=True)
class ShelfSystemBalluff:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        active (Union[Unset, bool]):
        io_link_master_id (Union[Unset, str]):
        shelf_system_status (Union[Unset, ShelfSystemBalluffShelfSystemStatus]):
        current_color (Union[Unset, ShelfSystemBalluffCurrentColor]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    io_link_master_id: Union[Unset, str] = UNSET
    shelf_system_status: Union[Unset, ShelfSystemBalluffShelfSystemStatus] = UNSET
    current_color: Union[Unset, ShelfSystemBalluffCurrentColor] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        active = self.active
        io_link_master_id = self.io_link_master_id
        shelf_system_status: Union[Unset, str] = UNSET
        if not isinstance(self.shelf_system_status, Unset):
            shelf_system_status = self.shelf_system_status.value

        current_color: Union[Unset, str] = UNSET
        if not isinstance(self.current_color, Unset):
            current_color = self.current_color.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if active is not UNSET:
            field_dict["active"] = active
        if io_link_master_id is not UNSET:
            field_dict["ioLinkMasterId"] = io_link_master_id
        if shelf_system_status is not UNSET:
            field_dict["shelfSystemStatus"] = shelf_system_status
        if current_color is not UNSET:
            field_dict["currentColor"] = current_color

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        active = d.pop("active", UNSET)

        io_link_master_id = d.pop("ioLinkMasterId", UNSET)

        _shelf_system_status = d.pop("shelfSystemStatus", UNSET)
        shelf_system_status: Union[Unset, ShelfSystemBalluffShelfSystemStatus]
        if isinstance(_shelf_system_status, Unset):
            shelf_system_status = UNSET
        else:
            shelf_system_status = ShelfSystemBalluffShelfSystemStatus(_shelf_system_status)

        _current_color = d.pop("currentColor", UNSET)
        current_color: Union[Unset, ShelfSystemBalluffCurrentColor]
        if isinstance(_current_color, Unset):
            current_color = UNSET
        else:
            current_color = ShelfSystemBalluffCurrentColor(_current_color)

        shelf_system_balluff = cls(
            id=id,
            name=name,
            active=active,
            io_link_master_id=io_link_master_id,
            shelf_system_status=shelf_system_status,
            current_color=current_color,
        )

        shelf_system_balluff.additional_properties = d
        return shelf_system_balluff

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
