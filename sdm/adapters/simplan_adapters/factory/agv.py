from sdm.adapters.simplan_adapters.factory.item import ItemFactory
from sdm.adapters.simplan_adapters.reference_model_wrapper import ReferenceModelWrapper
from sdm.models.sdm_reference_model.reference_model import Resource
from sdm.models.simplan.model import AbstractNodeItem


class AGVFactory(ItemFactory):
    def __init__(self, ref_model: ReferenceModelWrapper):
        super().__init__(ref_model)
        self.instance = None

    def create(self, resource: Resource, common: dict) -> AbstractNodeItem:
        if self.instance is None:
            base = {
                **common,
                "class": "agvPool",
                "nodeName": "AGVPool",
                "parameters": [
                    {"class": "v_iNumAGVs", "type": "number", "value": 0},
                    {"class": "v_bParkWhenIdle", "type": "boolean", "value": False},
                    {"class": "v_rDriveSpeed", "type": "number", "value": 1},
                    {"class": "v_rRotateSpeed", "type": "number", "value": 30},
                    {"class": "v_rAcceleration", "type": "number", "value": -1},
                ],
            }
            self.instance = AbstractNodeItem.parse_obj(base)
        num_agvs = next(
            (p for p in self.instance.parameters if p.class_ == "v_iNumAGVs")
        )
        num_agvs.value = num_agvs.value + 1 if isinstance(num_agvs.value, int) else 1
        return self.instance
