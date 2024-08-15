import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.order_order_state import OrderOrderState
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.part_to_pick import PartToPick


T = TypeVar("T", bound="Order")


@attr.s(auto_attribs=True)
class Order:
    """
    Attributes:
        id (Union[Unset, str]):
        variant_id (Union[Unset, str]):
        amount (Union[Unset, int]):
        pole_housing_length_of_variant (Union[Unset, str]):
        priority_level (Union[Unset, int]):
        actice_training_id (Union[Unset, str]):
        active_game_round_id (Union[Unset, str]):
        parts_to_pick (Union[Unset, List['PartToPick']]):
        pole_housing_ids (Union[Unset, List[str]]):
        finished_pole_housing_ids (Union[Unset, List[str]]):
        order_state (Union[Unset, OrderOrderState]):
        on_picking (Union[Unset, bool]):
        on_matching (Union[Unset, bool]):
        at_entry_point (Union[Unset, bool]):
        passed_entry_point (Union[Unset, bool]):
        order_is_finished (Union[Unset, bool]):
        deleted (Union[Unset, bool]):
        time_stamp (Union[Unset, datetime.datetime]):
        delivery_time (Union[Unset, datetime.datetime]):
        completion_time (Union[Unset, datetime.datetime]):
        good_parts (Union[Unset, int]):
        faulty_parts (Union[Unset, int]):
    """

    id: Union[Unset, str] = UNSET
    variant_id: Union[Unset, str] = UNSET
    amount: Union[Unset, int] = UNSET
    pole_housing_length_of_variant: Union[Unset, str] = UNSET
    priority_level: Union[Unset, int] = UNSET
    actice_training_id: Union[Unset, str] = UNSET
    active_game_round_id: Union[Unset, str] = UNSET
    parts_to_pick: Union[Unset, List["PartToPick"]] = UNSET
    pole_housing_ids: Union[Unset, List[str]] = UNSET
    finished_pole_housing_ids: Union[Unset, List[str]] = UNSET
    order_state: Union[Unset, OrderOrderState] = UNSET
    on_picking: Union[Unset, bool] = UNSET
    on_matching: Union[Unset, bool] = UNSET
    at_entry_point: Union[Unset, bool] = UNSET
    passed_entry_point: Union[Unset, bool] = UNSET
    order_is_finished: Union[Unset, bool] = UNSET
    deleted: Union[Unset, bool] = UNSET
    time_stamp: Union[Unset, datetime.datetime] = UNSET
    delivery_time: Union[Unset, datetime.datetime] = UNSET
    completion_time: Union[Unset, datetime.datetime] = UNSET
    good_parts: Union[Unset, int] = UNSET
    faulty_parts: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        variant_id = self.variant_id
        amount = self.amount
        pole_housing_length_of_variant = self.pole_housing_length_of_variant
        priority_level = self.priority_level
        actice_training_id = self.actice_training_id
        active_game_round_id = self.active_game_round_id
        parts_to_pick: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.parts_to_pick, Unset):
            parts_to_pick = []
            for parts_to_pick_item_data in self.parts_to_pick:
                parts_to_pick_item = parts_to_pick_item_data.to_dict()

                parts_to_pick.append(parts_to_pick_item)

        pole_housing_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.pole_housing_ids, Unset):
            pole_housing_ids = self.pole_housing_ids

        finished_pole_housing_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.finished_pole_housing_ids, Unset):
            finished_pole_housing_ids = self.finished_pole_housing_ids

        order_state: Union[Unset, str] = UNSET
        if not isinstance(self.order_state, Unset):
            order_state = self.order_state.value

        on_picking = self.on_picking
        on_matching = self.on_matching
        at_entry_point = self.at_entry_point
        passed_entry_point = self.passed_entry_point
        order_is_finished = self.order_is_finished
        deleted = self.deleted
        time_stamp: Union[Unset, str] = UNSET
        if not isinstance(self.time_stamp, Unset):
            time_stamp = self.time_stamp.isoformat()

        delivery_time: Union[Unset, str] = UNSET
        if not isinstance(self.delivery_time, Unset):
            delivery_time = self.delivery_time.isoformat()

        completion_time: Union[Unset, str] = UNSET
        if not isinstance(self.completion_time, Unset):
            completion_time = self.completion_time.isoformat()

        good_parts = self.good_parts
        faulty_parts = self.faulty_parts

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if variant_id is not UNSET:
            field_dict["variantId"] = variant_id
        if amount is not UNSET:
            field_dict["amount"] = amount
        if pole_housing_length_of_variant is not UNSET:
            field_dict["poleHousingLengthOfVariant"] = pole_housing_length_of_variant
        if priority_level is not UNSET:
            field_dict["priorityLevel"] = priority_level
        if actice_training_id is not UNSET:
            field_dict["acticeTrainingId"] = actice_training_id
        if active_game_round_id is not UNSET:
            field_dict["activeGameRoundId"] = active_game_round_id
        if parts_to_pick is not UNSET:
            field_dict["partsToPick"] = parts_to_pick
        if pole_housing_ids is not UNSET:
            field_dict["poleHousingIds"] = pole_housing_ids
        if finished_pole_housing_ids is not UNSET:
            field_dict["finishedPoleHousingIds"] = finished_pole_housing_ids
        if order_state is not UNSET:
            field_dict["orderState"] = order_state
        if on_picking is not UNSET:
            field_dict["onPicking"] = on_picking
        if on_matching is not UNSET:
            field_dict["onMatching"] = on_matching
        if at_entry_point is not UNSET:
            field_dict["atEntryPoint"] = at_entry_point
        if passed_entry_point is not UNSET:
            field_dict["passedEntryPoint"] = passed_entry_point
        if order_is_finished is not UNSET:
            field_dict["orderIsFinished"] = order_is_finished
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if time_stamp is not UNSET:
            field_dict["timeStamp"] = time_stamp
        if delivery_time is not UNSET:
            field_dict["deliveryTime"] = delivery_time
        if completion_time is not UNSET:
            field_dict["completionTime"] = completion_time
        if good_parts is not UNSET:
            field_dict["goodParts"] = good_parts
        if faulty_parts is not UNSET:
            field_dict["faultyParts"] = faulty_parts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.part_to_pick import PartToPick

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        variant_id = d.pop("variantId", UNSET)

        amount = d.pop("amount", UNSET)

        pole_housing_length_of_variant = d.pop("poleHousingLengthOfVariant", UNSET)

        priority_level = d.pop("priorityLevel", UNSET)

        actice_training_id = d.pop("acticeTrainingId", UNSET)

        active_game_round_id = d.pop("activeGameRoundId", UNSET)

        parts_to_pick = []
        _parts_to_pick = d.pop("partsToPick", UNSET)
        for parts_to_pick_item_data in _parts_to_pick or []:
            parts_to_pick_item = PartToPick.from_dict(parts_to_pick_item_data)

            parts_to_pick.append(parts_to_pick_item)

        pole_housing_ids = cast(List[str], d.pop("poleHousingIds", UNSET))

        finished_pole_housing_ids = cast(List[str], d.pop("finishedPoleHousingIds", UNSET))

        _order_state = d.pop("orderState", UNSET)
        order_state: Union[Unset, OrderOrderState]
        if isinstance(_order_state, Unset):
            order_state = UNSET
        else:
            order_state = OrderOrderState(_order_state)

        on_picking = d.pop("onPicking", UNSET)

        on_matching = d.pop("onMatching", UNSET)

        at_entry_point = d.pop("atEntryPoint", UNSET)

        passed_entry_point = d.pop("passedEntryPoint", UNSET)

        order_is_finished = d.pop("orderIsFinished", UNSET)

        deleted = d.pop("deleted", UNSET)

        _time_stamp = d.pop("timeStamp", UNSET)
        time_stamp: Union[Unset, datetime.datetime]
        if isinstance(_time_stamp, Unset):
            time_stamp = UNSET
        else:
            time_stamp = isoparse(_time_stamp)

        _delivery_time = d.pop("deliveryTime", UNSET)
        delivery_time: Union[Unset, datetime.datetime]
        if isinstance(_delivery_time, Unset):
            delivery_time = UNSET
        else:
            delivery_time = isoparse(_delivery_time)

        _completion_time = d.pop("completionTime", UNSET)
        completion_time: Union[Unset, datetime.datetime]
        if isinstance(_completion_time, Unset):
            completion_time = UNSET
        else:
            completion_time = isoparse(_completion_time)

        good_parts = d.pop("goodParts", UNSET)

        faulty_parts = d.pop("faultyParts", UNSET)

        order = cls(
            id=id,
            variant_id=variant_id,
            amount=amount,
            pole_housing_length_of_variant=pole_housing_length_of_variant,
            priority_level=priority_level,
            actice_training_id=actice_training_id,
            active_game_round_id=active_game_round_id,
            parts_to_pick=parts_to_pick,
            pole_housing_ids=pole_housing_ids,
            finished_pole_housing_ids=finished_pole_housing_ids,
            order_state=order_state,
            on_picking=on_picking,
            on_matching=on_matching,
            at_entry_point=at_entry_point,
            passed_entry_point=passed_entry_point,
            order_is_finished=order_is_finished,
            deleted=deleted,
            time_stamp=time_stamp,
            delivery_time=delivery_time,
            completion_time=completion_time,
            good_parts=good_parts,
            faulty_parts=faulty_parts,
        )

        order.additional_properties = d
        return order

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
