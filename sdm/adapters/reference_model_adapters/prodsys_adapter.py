from typing import List


from prodsys import adapters
from prodsys.models import (product_data, performance_indicators, performance_data, processes_data, resource_data, time_model_data, sink_data, source_data, state_data, scenario_data)
import prodsys

from sdm.models.sdm_reference_model import ReferenceModel
from sdm.models.sdm_reference_model import procedure, product, order, resources, processes, distribution, change_scenario
from sdm.models.prodsys.prodsys import ProdsysModel
from sdm.models.sdm_reference_model.performance import KPI, EventLog, KeyPerformanceIndicators, Performance

def transform_prodsys_model(prodsys_model: ProdsysModel) -> ReferenceModel:
    """
    Transforms a production system represented in the prodsys model to a sdm reference model.

    Args:
        prodsys_model (adapters.ProductionSystemAdapter): The prodsys model of a production system to transform.

    Returns:
        ReferenceModel: The transformed reference model of the production system.
    """
    # processes = transform_processes(prodsys_model)
    # products = transform_products(prodsys_model)
    # procedures = transform_procedures(prodsys_model)
    resources = transform_resources(prodsys_model)
    # orders = transform_orders(prodsys_model)
    # scenario = transform_scenario(prodsys_model)
    performance = transform_performance(prodsys_model)
    return ReferenceModel(
        resources,
        performance
    )

def transform_processes(prodsys_model: ProdsysModel) -> List[processes.Process]:
    """
    Transforms processes of a prodsys model to processes of a sdm reference model.

    Args:
        prodsys_model (ProdsysModel): The prodsys model to transform.

    Returns:
        List[processes.Process]: The transformed processes.
    """
    pass

def transform_products(prodsys_model: ProdsysModel) -> List[product.Product]:
    """
    Transforms products of a prodsys model to products of a sdm reference model.

    Args:
        prodsys_model (ProdsysModel): The prodsys model to transform.

    Returns:
        List[product.Product]: The transformed products.
    """
    pass

def transform_procedures(prodsys_model: ProdsysModel) -> List[procedure.Procedure]:
    """
    Transforms procedures of a prodsys model to procedures of a sdm reference model.

    Args:
        prodsys_model (ProdsysModel): The prodsys model to transform.

    Returns:
        List[procedure.Procedure]: The transformed procedures.
    """
    pass

def transform_resources(prodsys_model: ProdsysModel) -> List[resources.Resource]:
    """
    Transforms resources of a prodsys model to resources of a sdm reference model.

    Args:
        prodsys_model (ProdsysModel): The prodsys model to transform.

    Returns:
        List[resources.Resource]: The transformed resources.
    """
    prodsys_resources = prodsys_model.resource_data
    reference_model_resources = []
    for prodsys_resource in prodsys_resources:
        reference_model_resources.append(transform_resource(prodsys_resource))
    reference_model_resources.append(transform_production_system(prodsys_model))

    return reference_model_resources


def transform_resource(prodsys_resource: resource_data.RESOURCE_DATA_UNION) -> resources.Resource:
    """
    Transforms a resource of a prodsys model to a resource of a sdm reference model.

    Args:
        prodsys_resource (resource_data.Resource): The prodsys resource to transform.

    Returns:
        resources.Resource: The transformed resource.
    """
    control_policy = prodsys_resource.control_policy.value
    if "transport" in control_policy:
        control_policy = control_policy.split("_")[0]
    if isinstance(prodsys_resource, resource_data.ProductionResourceData):
        resource_type = "Manufacturing"
    elif isinstance(prodsys_resource, resource_data.TransportResourceData):
        resource_type = "Material Flow"
    else:
        raise ValueError(f"Unknown resource type {type(prodsys_resource)}")
    # TODO: create modules based on compound processes
    return resources.Resource(
        id=prodsys_resource.ID,
        description=prodsys_resource.description,
        capabilities=resources.Capabilities(
            id=f"{prodsys_resource.ID}_capabilities",
            description=f"Capabilities of {prodsys_resource.ID}",
            procedures_ids= prodsys_resource.process_ids + prodsys_resource.state_ids
        ),
        control_logic=resources.ControlLogic(
            id=f"{prodsys_resource.ID}_control_logic",
            description=f"Control logic of {prodsys_resource.ID}",
            sequencing_policy=control_policy
        ),
        resource_information=resources.ResourceInformation(
            id=f"{prodsys_resource.ID}_general_information",
            description=f"Resource information of {prodsys_resource.ID}",
            manufacturer="tbd",
            production_level="Station",
            resource_type=resource_type
        ),
    )

def get_subresources_of_production_system(prodsys_model: ProdsysModel, production_system_id: str) -> List[resources.SubResource]:
    sub_resources = []
    for resource in prodsys_model.resource_data:
        sub_resource = resources.SubResource(
            id_short=f"{production_system_id}_subresource_{resource.ID}",
            description=f"Subresource of {production_system_id} with id {resource.ID}",
            resource_id=resource.ID,
            position=resource.location,
            orientation=[0]
        )
        sub_resources.append(sub_resource)
    return sub_resources


def transform_production_system(prodsys_model: ProdsysModel) -> resources.Resource:
    """
    Transforms a resource of a prodsys model to a resource of a sdm reference model.

    Args:
        prodsys_resource (resource_data.Resource): The prodsys resource to transform.

    Returns:
        resources.Resource: The transformed resource.
    """
    production_system_id = prodsys_model.adapter.ID
    
    resource_configuration = resources.ResourceConfiguration(
        id=f"{production_system_id}_configuration",
        description=f"Configuration of {production_system_id}",
        sub_resources=get_subresources_of_production_system(prodsys_model, production_system_id)
    )

    resource_performances = resources.ResourcePerformances(
        id=f"{production_system_id}_performances",
        description=f"Performances of {production_system_id}",
        resource_performance=[
            resources.ResourcePerformance(
                id_short=f"{production_system_id}_performance_{prodsys_model.adapter.seed}",
                description=f"Performance of {production_system_id} with seed {prodsys_model.adapter.seed}",
                performance_id=f"performance_{production_system_id}_{prodsys_model.adapter.seed}",
                associated_configuration_id=f"{production_system_id}_configuration",
                obtained_performance_from="prodsys_" + prodsys.VERSION
            )
        ]
    )
    procedure_ids = []
    for resource in prodsys_model.resource_data:
        procedure_ids += resource.process_ids
        procedure_ids += resource.state_ids
    return resources.Resource(
        id=production_system_id,
        description=f"Resource with id {production_system_id}",
        capabilities=resources.Capabilities(
            id=f"{production_system_id}_capabilities",
            description=f"Capabilities of {production_system_id}",
            procedures_ids=procedure_ids
        ),
        control_logic=resources.ControlLogic(
            id=f"{production_system_id}_control_logic",
            description=f"Control logic of {production_system_id}",
            routing_policy="shortest_queue"
        ),
        resource_information=resources.ResourceInformation(
            id=f"{production_system_id}_general_information",
            description=f"Resource information of {production_system_id}",
            manufacturer="tbd",
            production_level="Station",
            resource_type="Manufacturing"
        ),
        resource_performances=resource_performances,
        resource_configuration=resource_configuration
    )

def transform_orders(prodsys_model: ProdsysModel) -> List[order.Order]:
    """
    Transforms orders of a prodsys model to orders of a sdm reference model.

    Args:
        prodsys_model (ProdsysModel): The prodsys model to transform.

    Returns:
        List[order.Order]: The transformed orders.
    """
    pass

def transform_scenario(prodsys_model: ProdsysModel) -> change_scenario.ChangeScenario:
    """
    Transforms the scenario of a prodsys model to a scenario of a sdm reference model.

    Args:
        prodsys_model (ProdsysModel): The prodsys model to transform.

    Returns:
        change_scenario.ChangeScenario: The transformed scenario.
    """
    pass

def get_key_performance_indicators(prodsys_model: ProdsysModel) -> KeyPerformanceIndicators:
    kpis = []
    prodsys_kpis: List[performance_indicators.KPI_UNION] = prodsys_model.get_models_of_type(performance_data.Performance).pop().kpis
    for kpi in prodsys_kpis:
        # print("__", tuple([context.value for context in kpi.context]))
        # context = tuple([context.value for context in kpi.context])
        # for i in range(len(context)):
        #     if context[i] == "all_m":
        #         context[i] = "procedure"
        reference_model_kpi = KPI(
            id_short=f"KPI_{prodsys_model.adapter.ID}_{prodsys_model.adapter.seed}_{id(kpi)}",
            description=f"KPI {kpi.name} of {prodsys_model.adapter.ID} with seed {prodsys_model.adapter.seed}",
            name=kpi.name,
            target=kpi.target,
            weight=kpi.weight,
            value=kpi.value,
            context=tuple([context.value for context in kpi.context]),
            resource=kpi.resource,
            product=kpi.product_type,
        )
        if hasattr(kpi, "process"):
            reference_model_kpi.process = kpi.process
        if hasattr(kpi, "start_time"):
            reference_model_kpi.start_time = kpi.start_time
        if hasattr(kpi, "end_time"):
            reference_model_kpi.end_time = kpi.end_time
    return KeyPerformanceIndicators(
        id=f"key_performance_indicators_{prodsys_model.adapter.ID}_{prodsys_model.adapter.seed}",
        description=f"Key performance indicators of {prodsys_model.adapter.ID} with seed {prodsys_model.adapter.seed}",
        kpis=kpis,
        )


map_prodsys_activity_type_to_reference_model_state_type = {
    "start state": "Start",
    "end state": "End",
    "start interrupt": "StartInterupt",
    "end interrupt": "EndInterupt",
    "created product": "Start",
    "finished product": "End",
}

def get_reference_model_activity_type(activity_type: str) -> str:
    """
    Transforms an activity type of a prodsys model to an activity type of a sdm reference model.

    Args:
        activity_type (str): The activity type to transform.

    Returns:
        str: The transformed activity type.
    """
    return map_prodsys_activity_type_to_reference_model_state_type[activity_type]

map_prodsys_state_type_to_reference_model_state_type = {
    state_data.StateTypeEnum.ProductionState: procedure.ProcedureTypeEnum.PRODUCTION,
    state_data.StateTypeEnum.SetupState: procedure.ProcedureTypeEnum.SETUP,
    state_data.StateTypeEnum.BreakDownState: procedure.ProcedureTypeEnum.BREAKDOWN,
    state_data.StateTypeEnum.TransportState: procedure.ProcedureTypeEnum.TRANSPORT,
    state_data.StateTypeEnum.ProcessBreakDownState: procedure.ProcedureTypeEnum.BREAKDOWN,
    "Source": procedure.ProcedureTypeEnum.ORDER_RELEASE,
    "Sink": procedure.ProcedureTypeEnum.ORDER_SHIPPING,
    "Transport": procedure.ProcedureTypeEnum.TRANSPORT,
    "Production": procedure.ProcedureTypeEnum.PRODUCTION,
    "Breakdown": procedure.ProcedureTypeEnum.BREAKDOWN,
}


def get_reference_model_procedure_type(state_type: str) -> str:
    """
    Transforms a state type of a prodsys model to a state type of a sdm reference model.

    Args:
        state_type (str): The state type to transform.

    Returns:
        str: The transformed state type.
    """
    return map_prodsys_state_type_to_reference_model_state_type[state_type]


def get_event_log(prodsys_model: ProdsysModel) -> List[procedure.Event]:
    event_log = []
    prodsys_event_log: List[performance_data.Event] = prodsys_model.get_models_of_type(procedure.Event)
    for event in prodsys_event_log:
        reference_model_event = procedure.Event(
            id_short=f"Event_{prodsys_model.adapter.ID}_{prodsys_model.adapter.seed}_{id(event)}",
            description=f"Event {event.time} of {prodsys_model.adapter.ID} with seed {prodsys_model.adapter.seed}",
            time=event.time,
            resource_id=event.resource,
            procedure_id=event.state,
            procedure_type=get_reference_model_procedure_type(event.state_type),
            activity=get_reference_model_activity_type(event.activity),
            product=event.product,
            expected_end_time=event.expected_end_time,
            success=True
        )
        event_log.append(reference_model_event)
    return EventLog(
        id=f"event_log_{prodsys_model.adapter.ID}_{prodsys_model.adapter.seed}",
        description=f"Event log of {prodsys_model.adapter.ID} with seed {prodsys_model.adapter.seed}",
        event_log=event_log
    )


def transform_performance(prodsys_model: ProdsysModel) -> Performance:
    """
    Transforms the performance of a prodsys model to a performance of a sdm reference model.

    Args:
        prodsys_model (ProdsysModel): The prodsys model to transform.

    Returns:
        distribution.Distribution: The transformed performance.
    """
    return Performance(
        id=f"performance_{prodsys_model.adapter.ID}_{prodsys_model.adapter.seed}",
        description=f"Performance of {prodsys_model.adapter.ID} with seed {prodsys_model.adapter.seed}",
        key_performance_indicators=get_key_performance_indicators(prodsys_model),
        event_log=get_event_log(prodsys_model)
    )