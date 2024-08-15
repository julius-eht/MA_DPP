from typing import List

from sdm.adapters.simplan_adapters.factory.item import ItemFactory
from sdm.adapters.simplan_adapters.reference_model_wrapper import ReferenceModelWrapper
from sdm.adapters.simplan_adapters.util import assure_defined
from sdm.models.sdm_reference_model.reference_model import Process, Product, Resource
from sdm.models.simplan.model import AbstractNodeItem


class SourceFactory(ItemFactory):
    def __init__(self, ref_model: ReferenceModelWrapper):
        super().__init__(ref_model)
        self.products = ref_model.products

    def create(self, resource: Resource, common: dict):
        base = {
            **common,
            "class": "source",
            "parameters": [
                {"class": "v_tiCycleTime", "type": "time", "value": 10},
                {"class": "v_sDistrCycleTime", "type": "enum", "value": "negexp"},
                {"class": "v_bUseProductionPlan", "type": "boolean", "value": False},
                {
                    "class": "t_TypeMix_Import",
                    "type": "tableGrid",
                    "value": {"rows": self.__create_type_mix()},
                },
                {
                    "class": "t_ProductionPlan_Import",
                    "type": "tableGrid",
                    "value": {"rows": []},
                },
                {"class": "v_bUseWorkPlan", "type": "boolean", "value": True},
                {
                    "class": "t_configWorkplan",
                    "type": "tableGrid",
                    "value": {"rows": self.__create_config_workplan()},
                },
                {"class": "v_bUseSchedule", "type": "boolean", "value": False},
                {
                    "class": "v_sModeRescheduling",
                    "type": "enum",
                    "value": "no rescheduling",
                },
                {
                    "class": "t_Schedule_Import",
                    "type": "tableGrid",
                    "value": {"rows": []},
                },
            ],
        }
        return AbstractNodeItem.parse_obj(base)

    def __create_type_mix(self) -> List[dict]:
        return [self.__create_type_mix_entry(product) for product in self.products]

    def __create_config_workplan(self) -> List[dict]:
        return [
            entry
            for product in self.products
            for entry in self.__create_config(product)
        ]

    def __create_type_mix_entry(self, product: Product) -> dict:
        return {
            "col_Frequency": 100 / len(self.ref_model.products),
            "col_Number": 1,
            "col_Name": assure_defined(
                product.product_information,
                message=f"Missing production_information for {product.id_short}",
            ).product_type,
        }

    def __create_config(self, product: Product) -> List[dict]:
        p_type = assure_defined(
            product.product_information,
            message=f"Missing production_information for {product.id_short}",
        ).product_type
        p_id = assure_defined(
            product.process_reference,
            f"Missing process_reference for {product.id_short}",
        ).process_id
        process = self.ref_model.get_model_of_type(p_id, Process)

        steps = []
        for step, sequence in enumerate(process.process_model.sequence or []):
            steps.append(
                {
                    "col_VariantTypes": p_type,
                    "col_StepNr": step +1,
                    "col_ResourceTaskId": sequence,
                    "col_ProcTime": -1,
                }
            )

        return steps
