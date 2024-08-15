from typing import Optional

from sdm.adapters.simplan_adapters.factory.agv import AGVFactory
from sdm.adapters.simplan_adapters.factory.desk import DeskFactory
from sdm.adapters.simplan_adapters.factory.item import ItemFactory
from sdm.adapters.simplan_adapters.factory.manufacturing import ManufacturingFactory
from sdm.adapters.simplan_adapters.factory.sink import SinkFactory
from sdm.adapters.simplan_adapters.factory.source import SourceFactory
from sdm.adapters.simplan_adapters.reference_model_wrapper import ReferenceModelWrapper
from sdm.models.sdm_reference_model.reference_model import Resource
from sdm.models.sdm_reference_model.resources import SubResource
from sdm.models.simplan.model import AbstractNodeItem


class NodeFactory:
    __factories: dict[str, ItemFactory]

    def __init__(
        self,
        ref_model: ReferenceModelWrapper,
    ):
        self.key = 0
        self.ref_model = ref_model
        self.resources = ref_model.resources
        self.__factories = {
            "Source": SourceFactory(ref_model),
            "Sink": SinkFactory(ref_model),
            "Manufacturing": ManufacturingFactory(ref_model),
            "Barrier": DeskFactory(ref_model),
            "Material Flow": AGVFactory(ref_model),
        }

    def create(self, resource: Resource) -> Optional[AbstractNodeItem]:
        resource_type = (
            resource.resource_information.resource_type
            if resource.resource_information is not None
            else None
        )

        if resource_type is None or resource_type == "Empty Spot":
            return None
        else:
            node = self.__factories[resource_type].create(
                resource, self.__common(resource)
            )
            self.key += 1
            return node

    def __common(self, resource: Resource) -> dict:
        [loc, angle] = self.__get_pos(resource)
        common = {
            "key": self.key,
            "loc": loc,
            "category": "item",
            "nodeName": resource.id_short,
            "photoNames": [],
            "imageTransform": {
                "angle": angle,
                "flip": {"flipX": False, "flipY": False},
            },
        }
        return common

    def __get_pos(self, lookup: Resource):
        for resource in self.resources:
            if resource.resource_configuration is not None:
                sub_resources = resource.resource_configuration.sub_resources or []
                sub_res: Optional[SubResource] = next(
                    (
                        sub_res
                        for sub_res in sub_resources
                        if sub_res.resource_id == lookup.id
                    ),
                    None,
                )
                if sub_res is not None:
                    return (
                        f"{sub_res.position[0] * 20} {sub_res.position[1] * 20}",
                        sub_res.orientation[0],
                    )
        raise ValueError("No subresource found for resource")
