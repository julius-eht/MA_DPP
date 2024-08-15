from typing import List
from prodsys import adapters
from prodsys.models import (product_data, processes_data, resource_data, time_model_data, sink_data, source_data, state_data, scenario_data)

from sdm.models.sdm_reference_model import ReferenceModel
from sdm.models.sdm_reference_model import procedure, product, order, resources, processes, distribution, change_scenario
from sdm.models.sdm_reference_model.matcher import Matcher, is_procedure_origin_of_setup, is_procedure_target_of_setup


def transform_reference_model(reference_model: ReferenceModel) -> adapters.JsonProductionSystemAdapter:
    """
    Transforms a production system represented in the sdm reference model to a prodsys model.

    Args:
        reference_model (ReferenceModel): The reference model to transform.

    Returns:
        adapters.JsonProductionSystemAdapter: The transformed production system model.
    """
    if not reference_model.change_scenario:
        raise ValueError("Reference model does not contain a change scenario.")
    if len(reference_model.change_scenario) > 1:
        raise ValueError("Reference model contains more than one change scenario.")
    time_models = transform_time_models(reference_model)

    processes = transform_processes(reference_model)
    processes += transform_process_modules(reference_model)
    products = transform_products(reference_model)
    states = transform_states(reference_model)
    resources = transform_resources(reference_model)
    sources = transform_sources(reference_model)
    sinks = transform_sinks(reference_model)
    scenario = transform_scenario(reference_model)

    adapter = adapters.JsonProductionSystemAdapter(
        ID=reference_model.change_scenario[0].id_short,
        time_model_data=time_models,
        state_data=states,
        process_data=processes,
        product_data=products,
        resource_data=resources,
        source_data=sources,
        sink_data=sinks,
        scenario_data=scenario,
    )
    return adapter



def transform_time_models(reference_model: ReferenceModel) -> List[time_model_data.TIME_MODEL_DATA]:
    """
    Transforms the time models of the reference model to prodsys time models.

    Args:
        reference_model (ReferenceModel): The reference model to transform.

    Returns:
        List[time_model_data.TIME_MODEL_DATA]: The transformed time models.
    """
    prodsys_time_models = []
    reference_model_time_models = reference_model.get_models_of_type_name("TimeModel")
    for reference_model_time_model in reference_model_time_models:
        prodsys_time_models.append(create_time_model(reference_model_time_model))
    
    products = reference_model.products
    orders = reference_model.orders
    ordered_quantity = {}
    for product in products:
        for order in orders:
            for ordered_product_type in order.ordered_products.ordered_products:
                if product.id_short == ordered_product_type.product_type:
                    if not product.id_short in ordered_quantity:
                        ordered_quantity[product.id_short] = 0
                    ordered_quantity[product.id_short] += ordered_product_type.target_quantity
    for product_type, quantity in ordered_quantity.items():
        prodsys_time_models.append(create_arrival_time_model(product_type, quantity))
    return prodsys_time_models


def create_time_model(reference_model_time_model: procedure.TimeModel) -> time_model_data.TIME_MODEL_DATA:
    """
    Creates a prodsys time model from a reference model time model.

    Args:
        reference_model_time_model (procedure.TimeModel): The reference model time model to transform.

    Returns:
        time_model_data.TIME_MODEL_DATA: The transformed prodsys time model.
    """
    if reference_model_time_model.type_ == "sequential":
        return time_model_data.SequentialTimeModelData(
            ID=reference_model_time_model.id_short,
            description=reference_model_time_model.description,
            sequence=reference_model_time_model.sequence,
        )
    elif reference_model_time_model.type_ == "distribution":
        location = reference_model_time_model.distribution_parameters.mean
        if hasattr(reference_model_time_model.distribution_parameters, "std"):
            scale = reference_model_time_model.distribution_parameters.std
        else:
            scale = 0
        return time_model_data.FunctionTimeModelData(
            ID=reference_model_time_model.id_short,
            description=reference_model_time_model.description,
            distribution_function=reference_model_time_model.distribution_type,
            location=location / 60, # convert from seconds to minutes
            scale=scale / 60,
        )
    elif reference_model_time_model.type_ == "distance_based":
        return time_model_data.ManhattanDistanceTimeModelData(
            ID=reference_model_time_model.id_short,
            description=reference_model_time_model.description,
            speed=reference_model_time_model.speed,
            reaction_time=reference_model_time_model.reaction_time,
        )
    else:
        raise ValueError(f"Unknown time model type {reference_model_time_model.type_}")
    

def create_arrival_time_model(product_type: str, quantity: int) -> time_model_data.FunctionTimeModelData:
    """
    Creates a prodsys arrival time model with an exponentially distributed function from a product type and quantity.

    Args:
        product_type (str): Type of product to arrive
        quantity (int): Quantity of products to arrive

    Returns:
        time_model_data.FunctionTimeModelData: The transformed prodsys arrival time model.
    """
    regared_time_length = 7 * 24 * 60
    arrival_rate = regared_time_length / quantity
    return time_model_data.FunctionTimeModelData(
        ID="arrival_time_model_" + product_type,
        description="arrival_time_model_" + product_type,
        distribution_function="exponential",
        location=arrival_rate,
        scale=0,
    )


def transform_processes(reference_model: ReferenceModel) -> List[processes_data.PROCESS_DATA_UNION]:
    """
    Transforms the processes of the reference model to prodsys processes.

    Args:
        reference_model (ReferenceModel): The reference model to transform.

    Returns:
        List[processes_data.PROCESSES_DATA]: The transformed processes.
    """
    prodsys_processes = []
    reference_model_processes = reference_model.processes
    reference_model_procedures = reference_model.procedures
    matcher = Matcher(reference_model_processes, reference_model_procedures)
    for reference_model_process in reference_model_processes:
        associated_procedures = matcher.get_matching_procedures(reference_model_process)
        if not associated_procedures:
            continue
        prodsys_processes += create_production_processes(reference_model_process, associated_procedures)

    transport_procedure = reference_model.get_model("transport_procedure")
    prodsys_processes.append(create_transport_process(transport_procedure))
    return prodsys_processes

def create_production_processes(reference_model_process: processes.Process, reference_model_procedures: List[procedure.Procedure]) -> List[processes_data.ProductionProcessData]:
    """
    Creates a prodsys process from a reference model process.

    Args:
        reference_model_process (processes.Process): The reference model process to transform.

    Returns:
        processes_data.PROCESSES_DATA: The transformed prodsys process.
    """
    prodsys_processes = []
    capability = reference_model_process.process_attributes.process_attributes[0].attribute_value
    prodsys_process = processes_data.RequiredCapabilityProcessData(
            ID=reference_model_process.id_short,
            description=reference_model_process.description,
            type="RequiredCapabilityProcesses",
            capability=capability
        )
    prodsys_processes.append(prodsys_process)
    for reference_model_procedure in reference_model_procedures:
        prodsys_process = processes_data.CapabilityProcessData(
            ID=reference_model_procedure.id_short,
            description=reference_model_procedure.description,
            time_model_id=reference_model_procedure.time_model.id_short,
            type="CapabilityProcesses",
            capability=capability
        )
        prodsys_processes.append(prodsys_process)
    return prodsys_processes

def create_transport_process(transport_procedure: procedure.Procedure) -> processes_data.TransportProcessData:
    """
    Creates a prodsys transport process from a reference model transport procedure.

    Args:
        transport_procedure (procedure.Procedure): The reference model transport procedure to transform.

    Returns:
        processes_data.TransportProcessData: The transformed prodsys transport process.
    """
    return processes_data.TransportProcessData(
        ID=transport_procedure.id_short,
        description=transport_procedure.description,
        time_model_id=transport_procedure.time_model.id_short,
        type="TransportProcesses",
    )

def transform_products(reference_model: ReferenceModel) -> List[product_data.ProductData]:
    """
    Transforms the products of the reference model to prodsys products.

    Args:
        reference_model (ReferenceModel): The reference model to transform.

    Returns:
        List[product_data.ProductData]: The transformed products.
    """
    prodsys_products = []
    reference_model_products = reference_model.products
    for reference_model_product in reference_model_products:
        process_model = reference_model.get_model(reference_model_product.process_reference.process_id)
        prodsys_products.append(create_product(reference_model_product, process_model))
    return prodsys_products

def create_product(reference_model_product: product.Product, product_process_model: processes.Process) -> product_data.ProductData:
    """
    Creates a prodsys product from a reference model product.

    Args:
        reference_model_product (product.Product): The reference model product to transform.

    Returns:
        product_data.ProductData: The transformed prodsys product.
    """
    return product_data.ProductData(
        ID=reference_model_product.id_short,
        description=reference_model_product.description,
        product_type=reference_model_product.id_short,
        processes=product_process_model.process_model.sequence,
        transport_process="transport_procedure"
    )

def transform_states(reference_model: ReferenceModel) -> List[state_data.STATE_DATA_UNION]:
    """
    Transforms the states of the reference model to prodsys states.

    Args:
        reference_model (ReferenceModel): The reference model to transform.

    Returns:
        List[state_data.StateData]: The transformed states.
    """
    prodsys_states = []
    reference_model_procedures = reference_model.procedures

    setup_state_procedures = [procedure for procedure in reference_model_procedures if procedure.procedure_information.procedure_type in ["Setup"]]
    for reference_model_procedure in setup_state_procedures:
        prodsys_states.append(create_setup_state(reference_model_procedure, reference_model))
    
    breakdown_states = [procedure for procedure in reference_model_procedures if procedure.procedure_information.procedure_type in ["Breakdown"]]
    maintenance_states = [procedure for procedure in reference_model_procedures if procedure.procedure_information.procedure_type in ["Maintenance"]]
    for reference_model_procedure in breakdown_states:
        for maintenance_state in maintenance_states:
            maintenance_resource_id = maintenance_state.id_short.split("_")[0]
            maintenance_resource_availibility_id = maintenance_state.id_short.split("_")[1]
            breakdown_resource_id = reference_model_procedure.id_short.split("_")[0]
            breakdown_resource_availibility_id = reference_model_procedure.id_short.split("_")[1]
            if maintenance_resource_id == breakdown_resource_id and maintenance_resource_availibility_id == breakdown_resource_availibility_id:
                prodsys_states.append(create_breakdown_state(reference_model_procedure, maintenance_state))
    return prodsys_states

def create_setup_state(setup_procedure: procedure.Procedure, reference_model: ReferenceModel) -> List[state_data.SetupStateData]:
    """
    Creates prodsys states from a reference model procedure.

    Args:
        reference_model_procedure (procedure.Procedure): The reference model procedure to transform.

    Returns:
        List[state_data.StateData]: The transformed prodsys states.
    """
    production_procedures = [procedure for procedure in reference_model.procedures if procedure.procedure_information.procedure_type == "Production"]
    resource_id = [attribute_predicate for attribute_predicate in setup_procedure.process_attributes.process_attributes if attribute_predicate.general_attribute == "Identifier" and attribute_predicate.attribute_carrier == "Resource"].pop().attribute_value
    resource: resources.Resource = reference_model.get_model(resource_id)
    relevant_production_procedures = [procedure for procedure in production_procedures if procedure.id_short in resource.capabilities.procedures_ids]
    
    origin_setups = [procedure for procedure in relevant_production_procedures if is_procedure_origin_of_setup(procedure, setup_procedure)]
    target_setups = [procedure for procedure in relevant_production_procedures if is_procedure_target_of_setup(procedure, setup_procedure)]

    if not len(origin_setups) == 1 or not len(target_setups) == 1:
        raise ValueError(f"Could not find matching production procedures for setup procedure {setup_procedure.id_short} with {len(origin_setups)} origins and {len(target_setups)} targets.")
    
    origin_setup = origin_setups.pop()
    target_setup = target_setups.pop()

    return state_data.SetupStateData(
        ID=setup_procedure.id_short,
        description=setup_procedure.description,
        time_model_id=setup_procedure.time_model.id_short,
        type="SetupState",
        origin_setup=origin_setup.id_short,
        target_setup=target_setup.id_short,
    )

def create_breakdown_state(breakdown_procedure: procedure.Procedure, maintenance_procedure: procedure.Procedure) -> state_data.BreakDownStateData:
    return state_data.BreakDownStateData(
        ID=breakdown_procedure.id_short,
        description=breakdown_procedure.description,
        time_model_id=breakdown_procedure.time_model.id_short,
        type="BreakDownState",
        repair_time_model_id=maintenance_procedure.time_model.id_short,
    )

def transform_resources(reference_model: ReferenceModel) -> List[resource_data.RESOURCE_DATA_UNION]:
    """
    Transforms the resources of the reference model to prodsys resources.

    Args:
        reference_model (ReferenceModel): The reference model to transform.

    Returns:
        List[resource_data.ResourceData]: The transformed resources.
    """
    reference_model_resources = reference_model.resources

    prodsys_production_resources = []
    reference_model_production_resources = [resource for resource in reference_model_resources if resource.resource_information.production_level == "Station" and resource.resource_information.resource_type == "Manufacturing"]
    for reference_model_resource in reference_model_production_resources:
        prodsys_production_resources.append(create_production_resource(reference_model_resource, reference_model))
    
    reference_model_transport_resources = [resource for resource in reference_model_resources if resource.resource_information.resource_type == "Material Flow"]
    prodsys_transport_resources = []
    for reference_model_resource in reference_model_transport_resources:
        prodsys_transport_resources.append(create_transport_resource(reference_model_resource, reference_model))
    
    return prodsys_production_resources + prodsys_transport_resources

def get_procedure_of_type(capabilities: List[procedure.Procedure], capability_type: str) -> List[procedure.Procedure]:
    return_capabilities = []
    for procedure in capabilities:
        if procedure.procedure_information.procedure_type == capability_type:
            return_capabilities.append(procedure)
    return return_capabilities

def create_production_resource(reference_model_resource: resources.Resource, reference_model: ReferenceModel) -> resource_data.ResourceData:
    """
    Creates a prodsys resource from a reference model resource.

    Args:
        reference_model_resource (resources.Resource): The reference model resource to transform.

    Returns:
        resource_data.ResourceData: The transformed prodsys resource.
    """
    for resource in reference_model.resources:
        if resource.resource_configuration:
            for sub_resource in resource.resource_configuration.sub_resources:
                if sub_resource.resource_id == reference_model_resource.id_short:
                    location = sub_resource.position
                    break
    procedure_ids = reference_model_resource.capabilities.procedures_ids
    resource_procedures = [reference_model.get_model(procedure_id) for procedure_id in procedure_ids]
    process_ids = [procedure.id_short for procedure in get_procedure_of_type(resource_procedures, "Production")]
    breakdown_ids = [procedure.id_short for procedure in get_procedure_of_type(resource_procedures, "Breakdown")]
    setup_ids = [procedure.id_short for procedure in get_procedure_of_type(resource_procedures, "Setup")]

    return resource_data.ProductionResourceData(
        ID=reference_model_resource.id_short,
        description=reference_model_resource.description,
        capacity=1,
        location=location,
        controller="PipelineController",
        control_policy=reference_model_resource.control_logic.sequencing_policy,
        process_ids=process_ids,
        state_ids=breakdown_ids + setup_ids,
    )



def transform_process_modules(reference_model: ReferenceModel) -> List[processes_data.CompoundProcessData]:
    reference_model_resources = reference_model.resources
    reference_model_process_modules = [resource for resource in reference_model_resources if resource.resource_information.production_level == "Module" and resource.resource_information.resource_type == "Manufacturing"]
    prodsys_process_modules = []
    for reference_model_process_module in reference_model_process_modules:
        prodsys_process_modules.append(create_process_module(reference_model_process_module, reference_model))


    prodsys_reduced_process_modules = []
    process_ids_set = set()
    for prodsys_process_module in prodsys_process_modules:
        if not tuple(prodsys_process_module.process_ids) in process_ids_set:
            prodsys_reduced_process_modules.append(prodsys_process_module)
            process_ids_set.add(tuple(prodsys_process_module.process_ids))
    return prodsys_reduced_process_modules

def create_process_module(reference_model_resource: resources.Resource, reference_model: ReferenceModel) -> processes_data.CompoundProcessData:
    """
    Creates a prodsys resource from a reference model resource.

    Args:
        reference_model_resource (resources.Resource): The reference model resource to transform.

    Returns:
        resource_data.ResourceData: The transformed prodsys resource.
    """
    procedure_ids = reference_model_resource.capabilities.procedures_ids
    resource_procedures = [reference_model.get_model(procedure_id) for procedure_id in procedure_ids]
    process_ids = [procedure.id_short for procedure in get_procedure_of_type(resource_procedures, "Production")]
    return processes_data.CompoundProcessData(
        ID=reference_model_resource.id_short,
        description=reference_model_resource.description,
        process_ids=process_ids,
        type="CompoundProcesses",
    )


def create_transport_resource(reference_model_resource: resources.Resource, reference_model: ReferenceModel) -> resource_data.ResourceData:
    for resource in reference_model.resources:
        if resource.resource_configuration:
            for sub_resource in resource.resource_configuration.sub_resources:
                if sub_resource.resource_id == reference_model_resource.id_short:
                    location = sub_resource.position
                    break
    procedure_ids = reference_model_resource.capabilities.procedures_ids
    resource_procedures = [reference_model.get_model(procedure_id) for procedure_id in procedure_ids]
    breakdown_ids = [procedure.id_short for procedure in get_procedure_of_type(resource_procedures, "Breakdown")]
    return resource_data.TransportResourceData(
            ID=reference_model_resource.id_short,
            description=reference_model_resource.description,
            capacity=1,
            location=location,
            controller="TransportController",
            control_policy="SPT_transport",
            process_ids=["transport_procedure"],
            state_ids=breakdown_ids,
        )

def transform_sources(reference_model: ReferenceModel) -> List[source_data.SourceData]:
    """
    Transforms the sources of the reference model to prodsys sources.

    Args:
        reference_model (ReferenceModel): The reference model to transform.

    Returns:
        List[source_data.SourceData]: The transformed sources.
    """
    prodsys_sources = []
    products = reference_model.products
    source_resource = [resource for resource in reference_model.resources if resource.resource_information.resource_type == "Source"][0]
    for resource in reference_model.resources:
        if resource.resource_configuration:
            for sub_resource in resource.resource_configuration.sub_resources:
                if sub_resource.resource_id == source_resource.id_short:
                    location = sub_resource.position
                    break
    for product in products:
        prodsys_sources.append(create_source(product, location))
    return prodsys_sources


def create_source(product: product.Product, location: List[float]) -> source_data.SourceData:
    """
    Creates a prodsys source from a reference model source.

    Args:
        reference_model_source (resources.Source): The reference model source to transform.

    Returns:
        source_data.SourceData: The transformed prodsys source.
    """
    product_type = product.id_short
    return source_data.SourceData(
        ID="source_" + product_type,
        description="source_" + product_type,
        location=location,
        product_type=product_type,
        time_model_id="arrival_time_model_" + product_type,
        routing_heuristic="shortest_queue",
    )

def transform_sinks(reference_model: ReferenceModel) -> List[sink_data.SinkData]:
    """
    Transforms the sinks of the reference model to prodsys sinks.

    Args:
        reference_model (ReferenceModel): The reference model to transform.

    Returns:
        List[sink_data.SinkData]: The transformed sinks.
    """
    prodsys_sinks = []
    products = reference_model.products
    sink_resource = [resource for resource in reference_model.resources if resource.resource_information.resource_type == "Sink"][0]
    for resource in reference_model.resources:
        if resource.resource_configuration:
            for sub_resource in resource.resource_configuration.sub_resources:
                if sub_resource.resource_id == sink_resource.id_short:
                    location = sub_resource.position
                    break
    for product in products:
        prodsys_sinks.append(create_sink(product, location))
    return prodsys_sinks

def create_sink(product: product.Product, location: List[float]) -> sink_data.SinkData:
    """
    Creates a prodsys sink from a reference model sink.

    Args:
        reference_model_sink (resources.Sink): The reference model sink to transform.

    Returns:
        sink_data.SinkData: The transformed prodsys sink.
    """
    return sink_data.SinkData(
        ID="sink_" + product.id_short,
        description="sink_" + product.id_short,
        location=location,
        product_type=product.id_short,
    )

def transform_scenario(reference_model: ReferenceModel) -> scenario_data.ScenarioData:
    """
    Transforms the scenario of the reference model to prodsys scenario.

    Args:
        reference_model (ReferenceModel): The reference model to transform.

    Returns:
        scenario_data.SCENARIO_DATA: The transformed scenario.
    """
    reference_model_scenario = reference_model.change_scenario[0]
    constraints = create_scenario_constraints(reference_model_scenario)
    info = create_scenario_info(reference_model_scenario)
    objectives = create_scenario_objectives(reference_model_scenario)
    options = create_scenario_options(reference_model_scenario, reference_model)
    return scenario_data.ScenarioData(
        ID="scenario",
        description="scenario",
        constraints=constraints,
        info=info,
        objectives=objectives,
        options=options,
    )


def create_scenario_constraints(reference_model_scenario: change_scenario.ChangeScenario) -> scenario_data.ScenarioConstrainsData:
    """
    Creates a prodsys scenario constraints from a reference model scenario.

    Args:
        reference_model_scenario (scenario_data.ChangeScenario): The reference model scenario to transform.

    Returns:
        scenario_data.ScenarioConstraints: The transformed prodsys scenario constraints.
    """
    return scenario_data.ScenarioConstrainsData(
        max_reconfiguration_cost=reference_model_scenario.reconfiguration_constraints.max_reconfiguration_cost,
        max_num_machines=reference_model_scenario.reconfiguration_constraints.max_number_of_machines,
        max_num_transport_resources=reference_model_scenario.reconfiguration_constraints.max_number_of_transport_resources,
        max_num_processes_per_machine=reference_model_scenario.reconfiguration_constraints.max_number_of_process_modules_per_resource,
    )

def create_scenario_info(reference_model_scenario: change_scenario.ChangeScenario) -> scenario_data.ScenarioInfoData:
    """
    Creates a prodsys scenario info from a reference model scenario.

    Args:
        reference_model_scenario (scenario_data.ChangeScenario): The reference model scenario to transform.

    Returns:
        scenario_data.ScenarioInfo: The transformed prodsys scenario info.
    """
    # TODO: resolve to get this data from the reference model!
    return scenario_data.ScenarioInfoData(
        machine_cost=120000,
        transport_resource_cost=100000,
        process_module_cost=8500,
        breakdown_cost=0.11,
        time_range=7*24*60,
        maximum_breakdown_time=180
    )

def create_scenario_objectives(reference_model_scenario: change_scenario.ChangeScenario) -> List[scenario_data.Objective]:
    """
    Creates a prodsys scenario objectives from a reference model scenario.

    Args:
        reference_model_scenario (scenario_data.ChangeScenario): The reference model scenario to transform.

    Returns:
        scenario_data.ScenarioObjectives: The transformed prodsys scenario objectives.
    """
    objectives = []
    for objective in reference_model_scenario.reconfiguration_objectives.objectives:
        objectives.append(scenario_data.Objective(
            name=objective.type,
            weight=objective.weight,
        ))

    return objectives

def create_scenario_options(reference_model_scenario: change_scenario.ChangeScenario, reference_model: ReferenceModel) -> scenario_data.ScenarioOptionsData:
    """
    Creates a prodsys scenario options from a reference model scenario.

    Args:
        reference_model_scenario (scenario_data.ChangeScenario): The reference model scenario to transform.

    Returns:
        scenario_data.ScenarioOptions: The transformed prodsys scenario options.
    """
    if reference_model_scenario.reconfiguration_options.reconfiguration_type == "full":
        transformations = ["production_capacity", "transport_capacity", "layout", "sequencing_logic", "routing_logic"]
    else:
        transformations = [reference_model_scenario.reconfiguration_options.reconfiguration_type]
    possible_positions = set()
    for resource in reference_model.resources:
        if resource.resource_configuration:
            for sub_resource in resource.resource_configuration.sub_resources:
                possible_positions.add(tuple(sub_resource.position))
    possible_positions = list(possible_positions)
    return scenario_data.ScenarioOptionsData(
        transformations=transformations,
        machine_controllers=reference_model_scenario.reconfiguration_options.machine_controllers,
        transport_controllers=reference_model_scenario.reconfiguration_options.transport_controllers,
        routing_heuristics=reference_model_scenario.reconfiguration_options.routing_heuristics,
        positions=possible_positions,
    )
