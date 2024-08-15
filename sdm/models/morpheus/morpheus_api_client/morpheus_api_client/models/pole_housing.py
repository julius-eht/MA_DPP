from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.pole_housing_pole_housing_type import PoleHousingPoleHousingType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.process_data import ProcessData


T = TypeVar("T", bound="PoleHousing")


@attr.s(auto_attribs=True)
class PoleHousing:
    """
    Attributes:
        id (Union[Unset, str]):
        pole_housing_type (Union[Unset, PoleHousingPoleHousingType]):
        training_id (Union[Unset, str]):
        game_round_id (Union[Unset, str]):
        variant_id (Union[Unset, str]):
        active_work_station_id (Union[Unset, str]):
        active_work_process_id (Union[Unset, str]):
        pole_housing_okay (Union[Unset, bool]):
        process_data_array (Union[Unset, List['ProcessData']]):
        defect_message (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    pole_housing_type: Union[Unset, PoleHousingPoleHousingType] = UNSET
    training_id: Union[Unset, str] = UNSET
    game_round_id: Union[Unset, str] = UNSET
    variant_id: Union[Unset, str] = UNSET
    active_work_station_id: Union[Unset, str] = UNSET
    active_work_process_id: Union[Unset, str] = UNSET
    pole_housing_okay: Union[Unset, bool] = UNSET
    process_data_array: Union[Unset, List["ProcessData"]] = UNSET
    defect_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        pole_housing_type: Union[Unset, str] = UNSET
        if not isinstance(self.pole_housing_type, Unset):
            pole_housing_type = self.pole_housing_type.value

        training_id = self.training_id
        game_round_id = self.game_round_id
        variant_id = self.variant_id
        active_work_station_id = self.active_work_station_id
        active_work_process_id = self.active_work_process_id
        pole_housing_okay = self.pole_housing_okay
        process_data_array: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.process_data_array, Unset):
            process_data_array = []
            for process_data_array_item_data in self.process_data_array:
                process_data_array_item = process_data_array_item_data.to_dict()

                process_data_array.append(process_data_array_item)

        defect_message = self.defect_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if pole_housing_type is not UNSET:
            field_dict["poleHousingType"] = pole_housing_type
        if training_id is not UNSET:
            field_dict["trainingId"] = training_id
        if game_round_id is not UNSET:
            field_dict["gameRoundId"] = game_round_id
        if variant_id is not UNSET:
            field_dict["variantId"] = variant_id
        if active_work_station_id is not UNSET:
            field_dict["activeWorkStationId"] = active_work_station_id
        if active_work_process_id is not UNSET:
            field_dict["activeWorkProcessId"] = active_work_process_id
        if pole_housing_okay is not UNSET:
            field_dict["poleHousingOkay"] = pole_housing_okay
        if process_data_array is not UNSET:
            field_dict["processDataArray"] = process_data_array
        if defect_message is not UNSET:
            field_dict["defectMessage"] = defect_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.process_data import ProcessData

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _pole_housing_type = d.pop("poleHousingType", UNSET)
        pole_housing_type: Union[Unset, PoleHousingPoleHousingType]
        if isinstance(_pole_housing_type, Unset):
            pole_housing_type = UNSET
        else:
            pole_housing_type = PoleHousingPoleHousingType(_pole_housing_type)

        training_id = d.pop("trainingId", UNSET)

        game_round_id = d.pop("gameRoundId", UNSET)

        variant_id = d.pop("variantId", UNSET)

        active_work_station_id = d.pop("activeWorkStationId", UNSET)

        active_work_process_id = d.pop("activeWorkProcessId", UNSET)

        pole_housing_okay = d.pop("poleHousingOkay", UNSET)

        process_data_array = []
        _process_data_array = d.pop("processDataArray", UNSET)
        for process_data_array_item_data in _process_data_array or []:
            process_data_array_item = ProcessData.from_dict(process_data_array_item_data)

            process_data_array.append(process_data_array_item)

        defect_message = d.pop("defectMessage", UNSET)

        pole_housing = cls(
            id=id,
            pole_housing_type=pole_housing_type,
            training_id=training_id,
            game_round_id=game_round_id,
            variant_id=variant_id,
            active_work_station_id=active_work_station_id,
            active_work_process_id=active_work_process_id,
            pole_housing_okay=pole_housing_okay,
            process_data_array=process_data_array,
            defect_message=defect_message,
        )

        pole_housing.additional_properties = d
        return pole_housing

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
