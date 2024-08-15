import re
from typing import Callable, List

from sdm.adapters.simplan_adapters.factory.item import ItemFactory
from sdm.adapters.simplan_adapters.reference_model_wrapper import ReferenceModelWrapper
from sdm.models.sdm_reference_model.distribution import ExponentialDistribution
from sdm.models.sdm_reference_model.processes import AttributePredicate
from sdm.models.sdm_reference_model.reference_model import Procedure, Process, Resource
from sdm.models.simplan.model import AbstractNodeItem


class ManufacturingFactory(ItemFactory):
    def __init__(self, ref_model: ReferenceModelWrapper):
        super().__init__(ref_model)
        self.resources = ref_model.resources
        self.procedures = ref_model.procedures
        self.ref_model = ref_model
        self.__mapping = {
            "Blackbox": self.__blackbox,
            "CESA3R": self.__ca3sar,
            "VirtualStation": self.__virtualstation,
        }

    def create(self, resource: Resource, common: dict):
        cad_file = (
            resource.construction_data.cad_file
            if resource.construction_data is not None
            else None
        )
        if cad_file is None:
            raise ValueError("No cad file found for manufacturing resource")
        else:
            return self.__mapping[cad_file](resource, common)

    def __blackbox(self, resource: Resource, common: dict):
        base = {
            **common,
            "class": "blackbox",
            "parameters": [
                *self.__create_base_parameters(resource),
                {"class": "v_iCapacityIn", "type": "number", "value": 1},
                {"class": "v_iCapacityOut", "type": "number", "value": 1},
            ],
        }
        return AbstractNodeItem.parse_obj(base)

    def __ca3sar(self, resource: Resource, common: dict):
        base = {
            **common,
            "class": "ca3sarCell",
            "parameters": [
                *self.__create_base_parameters(resource),
                {"class": "v_iWPCPortCapacity", "type": "number", "value": 1},
                {"class": "v_tiConveyingWPC", "type": "time", "value": 2},
            ],
        }
        return AbstractNodeItem.parse_obj(base)

    def __virtualstation(self, resource: Resource, common: dict):
        base = {
            **common,
            "class": "virtualCell",
            "parameters": [
                *self.__create_base_parameters(resource),
                {"class": "v_iWPCPortCapacity", "type": "number", "value": 1},
                {"class": "v_tiConveyingWPC", "type": "time", "value": 2},
            ],
        }
        return AbstractNodeItem.parse_obj(base)

    def __create_base_parameters(self, resource: Resource):
        return [
            {"class": "Label", "type": "string", "value": ""},
            {"class": "v_tiProcTime", "type": "time", "value": 10},
            {"class": "v_bUseSetupMatrix", "type": "boolean", "value": False},
            {"class": "v_tiSetupTime", "type": "time", "value": 0},
            {"class": "t_SetupMatrix", "type": "tableGrid", "value": {"rows": []}},
            {
                "class": "v_rAvailability",
                "type": "number",
                "value": self.__get_avail(resource),
            },
            {"class": "v_tiMTTR", "type": "time", "value": self.__get_mttr(resource)},
            {
                "class": "t_configResources",
                "type": "tableGrid",
                "value": {"rows": self.__get_config_resources(resource)},
            },
            {
                "class": "v_iMachineId",
                "type": "number",
                "value": self.__get_res_id(resource),
            },
        ]

    def __get_res_id(self, resource: Resource):
        # extract the numbers from resource.id
        id = re.findall(r"\d+", resource.id)
        id = "".join(id)

        return int(id)

    def __get_mttr(self, resource: Resource) -> float:
        maintenance_procedure = self.__find_procedures(
            resource, lambda p: p.procedure_information.procedure_type == "Maintenance"
        )
        if len(maintenance_procedure) != 1:
            raise ValueError(
                "No or more than one maintenance procedure found for resource"
            )

        distribution = maintenance_procedure[0].time_model.distribution_parameters
        if distribution is None or not isinstance(
            distribution, ExponentialDistribution
        ):
            raise ValueError("No distribution found for maintenance procedure")
        return distribution.mean

    def __get_mtbf(self, resource: Resource) -> float:
        breakdown_procedure = self.__find_procedures(
            resource, lambda p: p.procedure_information.procedure_type == "Breakdown"
        )
        if len(breakdown_procedure) != 1:
            raise ValueError(
                "No or more than one breakdown procedure found for resource"
            )

        distribution = breakdown_procedure[0].time_model.distribution_parameters
        if distribution is None or not isinstance(
            distribution, ExponentialDistribution
        ):
            raise ValueError("No distribution found for breakdown procedure")
        return distribution.mean

    def __get_avail(self, resource: Resource) -> float:
        mtbf = self.__get_mtbf(resource)
        mttr = self.__get_mttr(resource)
        return 100 * (mtbf / (mtbf + mttr))

    def __get_config_resources(self, resource: Resource) -> List[dict]:
        procedures = self.__find_procedures(
            resource, lambda p: p.procedure_information.procedure_type == "Production"
        )

        return [self.__resource_config_for_procedure(p) for p in procedures]

    def __resource_config_for_procedure(self, procedure: Procedure) -> dict:
        # error on no mean for distribution
        proc_time = getattr(procedure.time_model.distribution_parameters, "mean")

        process = self.__find_process_for_procedure(procedure)
        return {"col_ResourceTaskId": process.id_short, "col_ProcTime": proc_time}

    def __find_procedures(
        self, resource: Resource, filter: Callable[[Procedure], bool]
    ) -> List[Procedure]:
        procedures: List[Procedure] = [
            procedure
            for p_id in (
                resource.capabilities.procedures_ids
                if resource.capabilities is not None
                else []
            )
            if (procedure := self.ref_model.get_model_of_type(p_id, Procedure))
            is not None
            and filter(procedure)
        ]

        return procedures

    def __find_process_for_procedure(self, procedure: Procedure):
        attrs = procedure.process_attributes.process_attributes
        process = next(
            process
            for process in self.ref_model.processes
            if self.__match_process_attrs(process, attrs)
        )
        return process

    def __match_process_attrs(
        self, process: Process, attrs: List[AttributePredicate]
    ) -> bool:
        process_attrs = process.process_attributes.process_attributes
        match = True
        for attr in attrs:
            process_attr = next(
                (
                    a
                    for a in process_attrs
                    if a.general_attribute == attr.general_attribute
                ),
                None,
            )
            if process_attr is None:
                match = False
                break
            else:
                if (
                    process_attr.predicate_type != attr.predicate_type
                    and process_attr.predicate_type != "equals"
                ):
                    match = False
                    break

                if process_attr.attribute_value != attr.attribute_value:
                    match = False
                    break

        return match
