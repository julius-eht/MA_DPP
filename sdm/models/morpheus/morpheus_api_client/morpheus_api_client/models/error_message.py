from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ErrorMessage")


@attr.s(auto_attribs=True)
class ErrorMessage:
    """
    Attributes:
        id (Union[Unset, str]):
        error (Union[Unset, str]):
        workstation (Union[Unset, str]):
        workstation_ip (Union[Unset, str]):
        time (Union[Unset, str]):
        gameround (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    workstation: Union[Unset, str] = UNSET
    workstation_ip: Union[Unset, str] = UNSET
    time: Union[Unset, str] = UNSET
    gameround: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        error = self.error
        workstation = self.workstation
        workstation_ip = self.workstation_ip
        time = self.time
        gameround = self.gameround

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if error is not UNSET:
            field_dict["error"] = error
        if workstation is not UNSET:
            field_dict["workstation"] = workstation
        if workstation_ip is not UNSET:
            field_dict["workstationIp"] = workstation_ip
        if time is not UNSET:
            field_dict["time"] = time
        if gameround is not UNSET:
            field_dict["gameround"] = gameround

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        error = d.pop("error", UNSET)

        workstation = d.pop("workstation", UNSET)

        workstation_ip = d.pop("workstationIp", UNSET)

        time = d.pop("time", UNSET)

        gameround = d.pop("gameround", UNSET)

        error_message = cls(
            id=id,
            error=error,
            workstation=workstation,
            workstation_ip=workstation_ip,
            time=time,
            gameround=gameround,
        )

        error_message.additional_properties = d
        return error_message

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
