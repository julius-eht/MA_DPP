from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.work_station_automation_degree import WorkStationAutomationDegree
from ..models.work_station_work_station_status import WorkStationWorkStationStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkStation")


@attr.s(auto_attribs=True)
class WorkStation:
    """
    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        manual (Union[Unset, str]):
        automation_degree (Union[Unset, WorkStationAutomationDegree]):
        image_url (Union[Unset, str]):
        buffer_type (Union[Unset, str]):
        buffer_size (Union[Unset, int]):
        work_process_ids (Union[Unset, List[str]]):
        power_consumption (Union[Unset, float]):
        carbon_footprint (Union[Unset, float]):
        editable_manual_id (Union[Unset, str]):
        io_link_master_id (Union[Unset, str]):
        current_work_process_id (Union[Unset, str]):
        current_pole_housing_id (Union[Unset, str]):
        pole_housing_in_station (Union[Unset, bool]):
        work_station_connected (Union[Unset, bool]):
        work_station_status (Union[Unset, WorkStationWorkStationStatus]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    manual: Union[Unset, str] = UNSET
    automation_degree: Union[Unset, WorkStationAutomationDegree] = UNSET
    image_url: Union[Unset, str] = UNSET
    buffer_type: Union[Unset, str] = UNSET
    buffer_size: Union[Unset, int] = UNSET
    work_process_ids: Union[Unset, List[str]] = UNSET
    power_consumption: Union[Unset, float] = UNSET
    carbon_footprint: Union[Unset, float] = UNSET
    editable_manual_id: Union[Unset, str] = UNSET
    io_link_master_id: Union[Unset, str] = UNSET
    current_work_process_id: Union[Unset, str] = UNSET
    current_pole_housing_id: Union[Unset, str] = UNSET
    pole_housing_in_station: Union[Unset, bool] = UNSET
    work_station_connected: Union[Unset, bool] = UNSET
    work_station_status: Union[Unset, WorkStationWorkStationStatus] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        manual = self.manual
        automation_degree: Union[Unset, str] = UNSET
        if not isinstance(self.automation_degree, Unset):
            automation_degree = self.automation_degree.value

        image_url = self.image_url
        buffer_type = self.buffer_type
        buffer_size = self.buffer_size
        work_process_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.work_process_ids, Unset):
            work_process_ids = self.work_process_ids

        power_consumption = self.power_consumption
        carbon_footprint = self.carbon_footprint
        editable_manual_id = self.editable_manual_id
        io_link_master_id = self.io_link_master_id
        current_work_process_id = self.current_work_process_id
        current_pole_housing_id = self.current_pole_housing_id
        pole_housing_in_station = self.pole_housing_in_station
        work_station_connected = self.work_station_connected
        work_station_status: Union[Unset, str] = UNSET
        if not isinstance(self.work_station_status, Unset):
            work_station_status = self.work_station_status.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if manual is not UNSET:
            field_dict["manual"] = manual
        if automation_degree is not UNSET:
            field_dict["automationDegree"] = automation_degree
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if buffer_type is not UNSET:
            field_dict["bufferType"] = buffer_type
        if buffer_size is not UNSET:
            field_dict["bufferSize"] = buffer_size
        if work_process_ids is not UNSET:
            field_dict["workProcessIds"] = work_process_ids
        if power_consumption is not UNSET:
            field_dict["powerConsumption"] = power_consumption
        if carbon_footprint is not UNSET:
            field_dict["carbonFootprint"] = carbon_footprint
        if editable_manual_id is not UNSET:
            field_dict["editableManualId"] = editable_manual_id
        if io_link_master_id is not UNSET:
            field_dict["ioLinkMasterId"] = io_link_master_id
        if current_work_process_id is not UNSET:
            field_dict["currentWorkProcessId"] = current_work_process_id
        if current_pole_housing_id is not UNSET:
            field_dict["currentPoleHousingId"] = current_pole_housing_id
        if pole_housing_in_station is not UNSET:
            field_dict["poleHousingInStation"] = pole_housing_in_station
        if work_station_connected is not UNSET:
            field_dict["workStationConnected"] = work_station_connected
        if work_station_status is not UNSET:
            field_dict["workStationStatus"] = work_station_status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        manual = d.pop("manual", UNSET)

        _automation_degree = d.pop("automationDegree", UNSET)
        automation_degree: Union[Unset, WorkStationAutomationDegree]
        if isinstance(_automation_degree, Unset):
            automation_degree = UNSET
        else:
            automation_degree = WorkStationAutomationDegree(_automation_degree)

        image_url = d.pop("imageUrl", UNSET)

        buffer_type = d.pop("bufferType", UNSET)

        buffer_size = d.pop("bufferSize", UNSET)

        work_process_ids = cast(List[str], d.pop("workProcessIds", UNSET))

        power_consumption = d.pop("powerConsumption", UNSET)

        carbon_footprint = d.pop("carbonFootprint", UNSET)

        editable_manual_id = d.pop("editableManualId", UNSET)

        io_link_master_id = d.pop("ioLinkMasterId", UNSET)

        current_work_process_id = d.pop("currentWorkProcessId", UNSET)

        current_pole_housing_id = d.pop("currentPoleHousingId", UNSET)

        pole_housing_in_station = d.pop("poleHousingInStation", UNSET)

        work_station_connected = d.pop("workStationConnected", UNSET)

        _work_station_status = d.pop("workStationStatus", UNSET)
        work_station_status: Union[Unset, WorkStationWorkStationStatus]
        if isinstance(_work_station_status, Unset):
            work_station_status = UNSET
        else:
            work_station_status = WorkStationWorkStationStatus(_work_station_status)

        work_station = cls(
            id=id,
            name=name,
            manual=manual,
            automation_degree=automation_degree,
            image_url=image_url,
            buffer_type=buffer_type,
            buffer_size=buffer_size,
            work_process_ids=work_process_ids,
            power_consumption=power_consumption,
            carbon_footprint=carbon_footprint,
            editable_manual_id=editable_manual_id,
            io_link_master_id=io_link_master_id,
            current_work_process_id=current_work_process_id,
            current_pole_housing_id=current_pole_housing_id,
            pole_housing_in_station=pole_housing_in_station,
            work_station_connected=work_station_connected,
            work_station_status=work_station_status,
        )

        work_station.additional_properties = d
        return work_station

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
