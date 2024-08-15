from typing import List, Optional, Dict


from sdm.models.sdm_reference_model import ReferenceModel, processes, product, procedure, resources, order, distribution, change_scenario
from sdm.models.flexisv1 import flexisv1
from sdm.model_core.data_model import DataModel

def transform_flexis_to_reference_model(flexis_model: DataModel) -> ReferenceModel:
    """
    Transform a flexis data model to a reference model.

    Args:
        flexis_model (DataModel): _description_

    Returns:
        ReferenceModel: _description_
    """
    processes = transform_processes(flexis_model)
    products = transform_products(flexis_model)
    procedures = transform_procedures(flexis_model)
    resources = transform_resources(flexis_model)
    orders = transform_orders(flexis_model)
    scenario = transform_scenario(flexis_model)
    return ReferenceModel(
        processes,
        products,
        procedures,
        resources,
        orders,
        scenario
    )


def transform_processes(flexis_data_model: DataModel) -> List[processes.Process]:
    """
    Transform a flexis process to a reference model process.

    Args:
        process_time (flexisv1_nested.ProcessTime): The process time that needs to be mapped to a process
        flexis_data_model (DataModel): The flexis data model that contains all the information

    Returns:
        processes.Process: The reference model process
    """
    processes = []
    tasks = flexis_data_model.get_models_of_type(flexisv1.Task)
    workplans = flexis_data_model.get_models_of_type(flexisv1.WorkPlan)
    workplan_tasks = flexis_data_model.get_models_of_type(flexisv1.WorkPlanTask)

    required_tasks = [workplan_task.task_id for workplan_task in workplan_tasks]
    relevant_tasks = [task for task in tasks if task.id_short in required_tasks]
    
    processes += [create_single_process_AAS(task) for task in relevant_tasks]
    processes += [
        create_workplan_process_AAS(workplan, workplan_tasks, processes)
        for workplan in workplans
    ]
    return processes

def create_single_process_AAS(task: flexisv1.Task) -> processes.Process:
    if "Pruefung" in task.name:
        assembly_process_type = "Testing"
    elif "Befettung" in task.name:
        assembly_process_type = "Special Operations"
    else:
        assembly_process_type = "Joining"
    return processes.Process(
        id=f"{task.id_short}_process",
        description=task.description,
        process_information=processes.ProcessInformation(
            id=f"{task.id_short}_process_info",
            description=f"General information of task {task.id_short}",
            general_type="Assembly",
            assembly_process_type=assembly_process_type,
        ),
        process_model=processes.ProcessModel(
            id=f"{task.id_short}_process_model",
            description=f"Process model of task {task.id_short}",
            type_=processes.ProcessModelType.SINGLE_PROCESS,
        ),
        process_attributes=processes.ProcessAttributes(
            id=f"{task.id_short}_process_attributes",
            description=f"Process Attributes of task {task.id_short}",
            process_attributes=[
                processes.AttributePredicate(
                    id_short=f"{task.id_short}_capability",
                    description=f"Capability Attribute Predicate of task {task.id_short}",
                    attribute_carrier="Module",
                    general_attribute="Capability",
                    predicate_type="equals",
                    attribute_value=task.name[8:],
                ),
                processes.AttributePredicate(
                    id_short=f"{task.id_short}_product_type",
                    description=f"Product Type Attribute Predicate of task {task.id_short}",
                    attribute_carrier="Module",
                    general_attribute="ProductType",
                    predicate_type="equals",
                    attribute_value=task.name[:5],
                ),
            ],
        ),
    )


def create_workplan_process_AAS(
    workplan: flexisv1.WorkPlan,
    workplan_task_data: List[flexisv1.WorkPlanTask],
    subprocesses: List[processes.Process],
) -> processes.Process:
    relevant_workplan_task_data = [
        workplan_task
        for workplan_task in workplan_task_data
        if workplan_task.work_plan_id == workplan.id_short
    ]
    relevant_workplan_task_data.sort(key=lambda x: x.sequence)
    task_id_sequence = [
        workplan_task.task_id + "_process" for workplan_task in relevant_workplan_task_data
    ]
    attribute_predicates_of_sub_processes = [
        process.process_attributes.process_attributes[0]
        for process in subprocesses
        if any(process.id_short == task_id for task_id in task_id_sequence)
    ]
    return processes.Process(
        id=f"{workplan.id_short}_process",
        description=f"Workplan of product {workplan.name}",
        process_information=processes.ProcessInformation(
            id=f"{workplan.id_short}_process_info",
            description=f"General information of workplan {workplan.name}",
            general_type="Assembly",
        ),
        process_model=processes.ProcessModel(
            id=f"{workplan.id_short}_process_model",
            description=f"Process model of workplan {workplan.name}",
            type_=processes.ProcessModelType.SEQUENTIAL_PROCESS_MODEL,
            sequence=task_id_sequence,
        ),
        process_attributes=processes.ProcessAttributes(
            id=f"{workplan.id_short}_process_attributes",
            description=f"Process Attributes of workplan {workplan.name}",
            process_attributes=attribute_predicates_of_sub_processes,
        ),
    )

def transform_products(flexis_data_model: DataModel) -> List[product.Product]:
    products = []
    workplans = flexis_data_model.get_models_of_type(flexisv1.WorkPlan)
    for workplan in workplans:
        products.append(create_product_AAS(workplan))
    return products

def create_product_AAS(workplan: flexisv1.WorkPlan) -> product.Product:
    return product.Product(
        id=f"{workplan.id_short}_product",
        description=f"Master product of type {workplan.name} containing all information every product of this type has.",
        product_information=product.ProductInformation(
            id=f"{workplan.id_short}_general_information",
            description=f"General Information for product {workplan.name}",
            product_type=workplan.name,
            manufacturer="Bosch GmbH",
        ),
        process_reference=product.ProcessReference(
            id=f"{workplan.id_short}_process_reference",
            description=f"Reference to the process to produce product {workplan.name}",
            process_id=f"{workplan.id_short}_process",
        ),
    )      

def transform_procedures(flexis_data_model: DataModel) -> List[procedure.Procedure]:
    procedures = []
    resource_ids = [resource.id_short for resource in flexis_data_model.get_models_of_type(flexisv1.Resource)]
    workplan_tasks = flexis_data_model.get_models_of_type(flexisv1.WorkPlanTask)
    required_tasks = [workplan_task.task_id for workplan_task in workplan_tasks]
    # 1. production procedures
    process_times = flexis_data_model.get_models_of_type(flexisv1.ProcessTime)
    relevant_process_times = [process_time for process_time in process_times if process_time.resource_id in resource_ids]
    relevant_process_times = [process_time for process_time in relevant_process_times if process_time.task_id in required_tasks]
    procedures += [create_production_procedure_AAS(process_time, flexis_data_model) for process_time in relevant_process_times]
    # 2. transport procedures
    procedures += [create_transport_procedure_AAS() for _ in range(1)]
    # 3. breakdown and maintenance procedures
    resource_availibilities = flexis_data_model.get_models_of_type(flexisv1.ResourceAvailibility)
    relevant_resource_availibilities = [resource_availibility for resource_availibility in resource_availibilities if resource_availibility.resource_id in resource_ids]
    procedures += [create_breakdown_procedure_AAS(resource_availibility, flexis_data_model) for resource_availibility in relevant_resource_availibilities]
    procedures += [create_maintenance_procedure_AAS(resource_availibility, flexis_data_model) for resource_availibility in relevant_resource_availibilities]
    # 4. setup procedures
    setup_data = flexis_data_model.get_models_of_type(flexisv1.SetupTime)
    relevant_setup_data = [setup for setup in setup_data if setup.resource_id in resource_ids]
    relevant_setup_data = [setup for setup in relevant_setup_data if setup.task_from_id in required_tasks or setup.task_to_id in required_tasks]
    procedures += [create_setup_procedure_AAS(setup, flexis_data_model) for setup in relevant_setup_data]
    return procedures


def get_scheduled_events_of_process_time(process_time: flexisv1.ProcessTime, flexis_data_model: DataModel) -> List[procedure.Event]:
    task: flexisv1.Task = flexis_data_model.get_model(process_time.task_id)
    resource: flexisv1.Resource = flexis_data_model.get_model(process_time.resource_id)

    referencing_job_tasks = flexis_data_model.get_referencing_models_of_type(task, flexisv1.JobTask)
    referencing_scheduled_job_tasks = flexis_data_model.get_referencing_models_of_type(resource, flexisv1.ScheduledJobTask)

    job_task_ids = set([job_task.id_short for job_task in referencing_job_tasks])
    scheduled_job_tasks = [scheduled_job_task for scheduled_job_task in referencing_scheduled_job_tasks if scheduled_job_task.job_task_id in job_task_ids]

    scheduled_events = []
    
    for scheduled_job_task in scheduled_job_tasks:
        job_task = [job_task for job_task in referencing_job_tasks if job_task.id_short == scheduled_job_task.job_task_id][0]
        job: flexisv1.Job = flexis_data_model.get_model(job_task.job_id)
        scheduled_events.append(procedure.Event(
            id_short=f"{job.id_short}_{job_task.id_short}_scheduled_event",
            description=f"Scheduled event of job {job.id_short} with job task {job_task.id_short}",
            procedure_type=procedure.ProcedureTypeEnum.PRODUCTION,
            activity=procedure.ActivityTypeEnum.START,
            time=scheduled_job_task.process_begin_date,
            expected_end_time=scheduled_job_task.process_end_date,
            resource_id=resource.id_short + "_resource",
            procedure_id=f"{task.id_short}_{process_time.id_short}_procedure",
            product_id=f"{job.id_short}_order",
        ))
    return scheduled_events


def create_production_procedure_AAS(
         process_time: flexisv1.ProcessTime,
         flexis_data_model: DataModel,
    ) -> procedure.Procedure:
    task: flexisv1.Task = flexis_data_model.get_model(process_time.task_id)
    scheduled_events = get_scheduled_events_of_process_time(process_time, flexis_data_model)
    return procedure.Procedure(
        id=f"{task.id_short}_{process_time.id_short}_procedure",
        description=f"Procedure data of task {task.id_short} with name {task.name} of resource {process_time.resource_id} with process time {process_time.id_short}",
        procedure_information=procedure.ProcedureInformation(
            id=f"{task.id_short}_{process_time.id_short}_procedure_information",
            description=f"Procedure information of task {task.id_short} with name {task.name} of resource {process_time.resource_id} with process time {process_time.id_short}",
            procedure_type=procedure.ProcedureTypeEnum.PRODUCTION,
        ),
        process_attributes=processes.ProcessAttributes(
            id=f"{task.id_short}_{process_time.id_short}_process_attributes",
            description=f"Process Attributes of task {task.id_short} and process time {process_time.id_short}",
            process_attributes=[
                processes.AttributePredicate(
                    id_short=f"{task.id_short}_{process_time.id_short}_capability",
                    description=f"Capability of task {task.id_short} with process time {process_time.id_short}",
                    attribute_carrier="Module",
                    general_attribute="Capability",
                    predicate_type="equals",
                    attribute_value=task.name[8:],
                ),
                processes.AttributePredicate(
                    id_short=f"{task.id_short}_{process_time.id_short}_product_type",
                    description=f"Product type of task {task.id_short} with process time {process_time.id_short}",
                    attribute_carrier="Module",
                    general_attribute="ProductType",
                    predicate_type="equals",
                    attribute_value=task.name[:5],
                ),
            ],
        ),
        execution_model=procedure.ExecutionModel(
            id=f"{task.id_short}_{process_time.id_short}_execution_model",
            description=f"Execution model of task {task.id_short} with name {task.name} of resource {process_time.resource_id} with process time {process_time.id_short}",
            schedule=scheduled_events
        ),
        time_model=procedure.TimeModel(
            id=f"{task.id_short}_{process_time.id_short}_time_model",
            description=f"Time model of procedure of task {task.id_short} with name {task.name} of resource {process_time.resource_id} with process time {process_time.id_short}",
            type_="distribution",
            distribution_type="normal",
            distribution_parameters=distribution.NormalDistribution(
                id_short=f"{task.id_short}_{process_time.id_short}_distribution_parameters",
                type="normal",
                mean=process_time.duration,
                std=process_time.duration / 10,
                ),
        ),
    )


def create_transport_procedure_AAS() -> procedure.Procedure:
    return procedure.Procedure(
        id=f"transport_procedure",
        description=f"Procedure to transport products",
        procedure_information=procedure.ProcedureInformation(
            id=f"transport_procedure_information",
            description=f"Procedure information of transport procedure",
            procedure_type=procedure.ProcedureTypeEnum.TRANSPORT,
        ),
        process_attributes=processes.ProcessAttributes(
            id=f"transport_procedure_process_attributes",
            description=f"Process Attributes of transport procedure",
            process_attributes=[
                processes.AttributePredicate(
                    id_short=f"transprot_procedure_attribute_predicate",
                    description=f"Attribute Predicate of transport procedure",
                    attribute_carrier="Transport",
                    general_attribute="Capability",
                    predicate_type="equals",
                    attribute_value="Transport",
                )
            ],
        ),
        time_model=procedure.TimeModel(
            id=f"transport_procedure_time_model",
            description=f"Time model of transport procedure",
            type_="distance_based",
            speed=60,  # meter per minute
            reaction_time=0.1,  # minutes
        ),
    )

def create_breakdown_procedure_AAS(resource_availibility: flexisv1.ResourceAvailibility, flexis_data_model: DataModel) -> procedure.Procedure:
    relevant_resource: flexisv1.Resource = flexis_data_model.get_model(resource_availibility.resource_id)
    return procedure.Procedure(
    id=f"{relevant_resource.id_short}_{resource_availibility.id_short}_breakdown_procedure",
    description=f"Procedure data of breakdown of resource {relevant_resource.id_short} with name {relevant_resource.name} with availibility {resource_availibility.id_short}.",
    procedure_information=procedure.ProcedureInformation(
        id=f"{relevant_resource.id_short}_{resource_availibility.id_short}_breakdown_procedure_information",
        description=f"Procedure information of breakdown of resource {relevant_resource.id_short} with name {relevant_resource.name} with availibility {resource_availibility.id_short}.",
        procedure_type=procedure.ProcedureTypeEnum.BREAKDOWN,
    ),
    process_attributes=processes.ProcessAttributes(
        id=f"{relevant_resource.id_short}_{resource_availibility.id_short}_breakdown_process_attributes",
        description=f"Process Attributes of breakdown of resource {relevant_resource.id_short} with name {relevant_resource.name} with availibility {resource_availibility.id_short}.",
        process_attributes=[
            processes.AttributePredicate(
                id_short=f"{relevant_resource.id_short}_{resource_availibility.id_short}_breakdown_attribute_predicate",
                description=f"Attribute Predicate of breakdown of resource {relevant_resource.id_short} with name {relevant_resource.name} with availibility {resource_availibility.id_short}.",
                attribute_carrier="Resource",
                general_attribute="Breakdown",
                predicate_type="equals",
                attribute_value=relevant_resource.id_short,
            )
        ],
    ),
    time_model=procedure.TimeModel(
        id=f"{relevant_resource.id_short}_{resource_availibility.id_short}_breakdown_time_model",
        description=f"Time model of procedure of breakdown of resource {relevant_resource.id_short} with name {relevant_resource.name} with availibility {resource_availibility.id_short}.",
        type_="distribution",
        distribution_type="exponential",
        distribution_parameters=distribution.ExponentialDistribution(
            id_short=f"{relevant_resource.id_short}_{resource_availibility.id_short}_breakdown_distribution_parameters",
            type="exponential",
            mean=resource_availibility.mttf,
        )
        ,
    ),
)

def create_maintenance_procedure_AAS(resource_availibility: flexisv1.ResourceAvailibility, flexis_data_model: DataModel) -> procedure.Procedure:
    relevant_resource: flexisv1.Resource = flexis_data_model.get_model(resource_availibility.resource_id)
    return procedure.Procedure(
    id=f"{relevant_resource.id_short}_{resource_availibility.id_short}_maintenance_procedure",
    description=f"Procedure data of maintenance of resource {relevant_resource.id_short} with name {relevant_resource.id_short} with availibility {resource_availibility.id_short}.",
    procedure_information=procedure.ProcedureInformation(
        id=f"{relevant_resource.id_short}_{resource_availibility.id_short}_maintenance_procedure_information",
        description=f"Procedure information of maintenance of resource {relevant_resource.id_short} with name {relevant_resource.name} with availibility {resource_availibility.id_short}.",
        procedure_type=procedure.ProcedureTypeEnum.MAINTENANCE,
    ),
    process_attributes=processes.ProcessAttributes(
        id=f"{relevant_resource.id_short}_{resource_availibility.id_short}_maintenance_process_attributes",
        description=f"Process Attributes of maintenance of resource {relevant_resource.id_short} with name {relevant_resource.name} with availibility {resource_availibility.id_short}.",
        process_attributes=[
            processes.AttributePredicate(
                id_short=f"{relevant_resource.id_short}_{resource_availibility.id_short}_maintenance_attribute_predicate",
                description=f"Attribute Predicate of maintenance of resource {relevant_resource.id_short} with name {relevant_resource.name} with availibility {resource_availibility.id_short}.",
                attribute_carrier="Resource",
                general_attribute="Maintenance",
                predicate_type="equals",
                attribute_value=relevant_resource.id_short,
            )
        ],
    ),
    time_model=procedure.TimeModel(
        id=f"{relevant_resource.id_short}_{resource_availibility.id_short}_maintenance_time_model",
        description=f"Time model of procedure of maintenance of resource {relevant_resource.id_short} with name {relevant_resource.name} with availibility {resource_availibility.id_short}.",
        type_="distribution",
        distribution_type="exponential",
        distribution_parameters=distribution.ExponentialDistribution(
            id_short=f"{relevant_resource.id_short}_{resource_availibility.id_short}_maintenance_distribution_parameters",
            type="exponential",
            mean=resource_availibility.mttr,
        ),
    ),
)

def create_setup_procedure_AAS(setup_time: flexisv1.SetupTime, flexis_data_model: DataModel) -> procedure.Procedure:
    relevant_resource: flexisv1.Resource = flexis_data_model.get_model(setup_time.resource_id)
    task_from = flexis_data_model.get_model(setup_time.task_from_id)
    task_to = flexis_data_model.get_model(setup_time.task_to_id)
    return procedure.Procedure(
    id=f"{relevant_resource.id_short}_{setup_time.id_short}_setup_procedure",
    description=f"Procedure data of setup of resource {relevant_resource.id_short} with name {relevant_resource.name} with setup {setup_time.id_short}.",
    procedure_information=procedure.ProcedureInformation(
        id=f"{relevant_resource.id_short}_{setup_time.id_short}_setup_procedure_information",
        description=f"Procedure information of setup of resource {relevant_resource.id_short} with name {relevant_resource.name} with setup {setup_time.id_short}.",
        procedure_type=procedure.ProcedureTypeEnum.SETUP,
    ),
    process_attributes=processes.ProcessAttributes(
        id=f"{relevant_resource.id_short}_{setup_time.id_short}_setup_process_attributes",
        description=f"Process Attributes of setup of resource {relevant_resource.id_short} with name {relevant_resource.name} with setup {setup_time.id_short}.",
        process_attributes=[
            processes.AttributePredicate(
                id_short=f"{relevant_resource.id_short}_{setup_time.id_short}_setup_attribute_predicate_resource",
                description=f"Attribute Predicate of setup of resource {relevant_resource.id_short} with name {relevant_resource.name} with setup {setup_time.id_short}.",
                attribute_carrier="Resource",
                general_attribute="Identifier",
                predicate_type="equals",
                attribute_value=relevant_resource.id_short + "_resource",
            ),
            processes.AttributePredicate(
                id_short=f"{relevant_resource.id_short}_{setup_time.id_short}_setup_attribute_predicate_capability_origin",
                description=f"Attribute Predicate of setup of resource {relevant_resource.id_short} with name {relevant_resource.name} with setup {setup_time.id_short}.",
                attribute_carrier="OriginModule",
                general_attribute="Capability",
                predicate_type="equals",
                attribute_value=task_from.name[8:],
            ),
            processes.AttributePredicate(
                id_short=f"{relevant_resource.id_short}_{setup_time.id_short}_setup_attribute_predicate_capability_target",
                description=f"Attribute Predicate of setup of resource {relevant_resource.id_short} with name {relevant_resource.name} with setup {setup_time.id_short}.",
                attribute_carrier="TargetModule",
                general_attribute="Capability",
                predicate_type="equals",
                attribute_value=task_to.name[8:],
            ),
            processes.AttributePredicate(
                id_short=f"{relevant_resource.id_short}_{setup_time.id_short}_setup_attribute_predicate_product_type_origin",
                description=f"Attribute Predicate of setup of resource {relevant_resource.id_short} with name {relevant_resource.name} with setup {setup_time.id_short}.",
                attribute_carrier="OriginModule",
                general_attribute="ProductType",
                predicate_type="equals",
                attribute_value=task_from.name[:5],
            ),
            processes.AttributePredicate(
                id_short=f"{relevant_resource.id_short}_{setup_time.id_short}_setup_attribute_predicate_product_type_target",
                description=f"Attribute Predicate of setup of resource {relevant_resource.id_short} with name {relevant_resource.name} with setup {setup_time.id_short}.",
                attribute_carrier="TargetModule",
                general_attribute="ProductType",
                predicate_type="equals",
                attribute_value=task_to.name[:5],
            ),
        ],
    ),
    time_model=procedure.TimeModel(
        id=f"{relevant_resource.id_short}_{setup_time.id_short}_setup_time_model",
        description=f"Time model of procedure of setup of resource {relevant_resource.id_short} with name {relevant_resource.name} with availibility {setup_time.id_short}.",
        type_="distribution",
        distribution_type="normal",
        distribution_parameters=distribution.NormalDistribution(
            id_short=f"{relevant_resource.id_short}_{setup_time.id_short}_setup_distribution_parameters",
            type="normal",
            mean=setup_time.duration,
            std=setup_time.duration / 10,
        ),
    ),
)

def transform_resources(flexis_data_model: DataModel) -> List[resources.Resource]:
    resource_data = flexis_data_model.get_models_of_type(flexisv1.Resource)
    resources = []
    for resource in resource_data:
        resources += create_resource_AAS(resource, flexis_data_model)

    return resources

def create_resource_information(resource: flexisv1.Resource) -> resources.ResourceInformation:
    resource_type = resource.type_id
    if resource_type == "resource_type_0":
        production_level = "Plant"
    elif resource_type == "resource_type_1":
        production_level = "System"
    else:
        production_level = "Station"

    if resource_type == "resource_type_3":
        resource_type = "Storage"
    elif resource_type == "resource_type_4":
        resource_type = "Material Flow"
    elif resource_type == "resource_type_5":
        resource_type = "Source"
    elif resource_type == "resource_type_6":
        resource_type = "Sink"
    elif resource_type == "resource_type_7":
        resource_type = "Barrier"
    elif resource_type == "resource_type_8":
        resource_type = "Empty Spot"
    else:
        resource_type = "Manufacturing"

    return resources.ResourceInformation(
        id=f"{resource.id_short}_general_information",
        description=f"General Information of resource {resource.id_short} with name {resource.name}",
        manufacturer="Bosch",
        production_level=production_level,
        resource_type=resource_type,
    )

def create_station_configuration(resource: flexisv1.Resource, flexis_data_model: DataModel) -> Optional[resources.ResourceConfiguration]:
    process_times_by_capability = get_process_times_by_capability(resource, flexis_data_model)
    if not process_times_by_capability:
        return None
    subresources = []
    for capability, process_times in process_times_by_capability.items():
        subresources.append(resources.SubResource(
            id_short=f"{resource.id_short}_subresource_{capability}",
            description=f"Subresource of resource {resource.id_short} with name {resource.name}",
            resource_id=f"{resource.id_short}_module_{capability}",
            position=[-1, -1],
            orientation=[-1],
            )
        )
    return resources.ResourceConfiguration(
        id=f"{resource.id_short}_resource_configuration",
        description=f"Resource configuration of resource {resource.id_short} with name {resource.name}",
        sub_resources=subresources,
    )

def create_resource_configuration(resource: flexisv1.Resource, flexis_data_model: DataModel) -> Optional[resources.ResourceConfiguration]:
    if resource.type_id not in ["resource_type_0", "resource_type_1", "resource_type_2"]:
        return None
    if resource.type_id == "resource_type_2":
        return create_station_configuration(resource, flexis_data_model)
    all_resources = flexis_data_model.get_models_of_type(flexisv1.Resource)
    child_resources = [potential_child_resource for potential_child_resource in all_resources if potential_child_resource.parent_id and potential_child_resource.parent_id == resource.id_short]
    subresources = []
    for child_resource in child_resources:
        if child_resource.type_id == "resource_type_1":
            location = [-1, -1]
            orientation = [-1]
        else:
            resource_position: flexisv1.Position = flexis_data_model.get_model(child_resource.position_id)
            location = [resource_position.x_coordinate, resource_position.y_coordinate]
            orientation = [resource_position.angle]
            
        subresources.append(resources.SubResource(
            id_short=f"{resource.id_short}_subresource_{child_resource.id_short}",
            description=f"Subresource of resource {resource.id_short} with name {resource.name}",
            resource_id=f"{child_resource.id_short}_resource",
            position=location,
            orientation=orientation,         
            )
        )
    return resources.ResourceConfiguration(
        id=f"{resource.id_short}_resource_configuration",
        description=f"Resource configuration of resource {resource.id_short} with name {resource.name}",
        sub_resources=subresources,
    )


def create_resource_AAS(
    resource: flexisv1.Resource,
    flexis_data_model: DataModel,
) -> List[resources.Resource]:
    relevant_process_times = flexis_data_model.get_referencing_models_of_type(resource, flexisv1.ProcessTime)
    relevant_availibility = flexis_data_model.get_referencing_models_of_type(resource, flexisv1.ResourceAvailibility)
    relevant_setup_times = flexis_data_model.get_referencing_models_of_type(resource, flexisv1.SetupTime)
    relevant_variants = flexis_data_model.get_referencing_models_of_type(resource, flexisv1.ResourceVariant)
    # Filter for relevant process times and setup times
    workplan_tasks = flexis_data_model.get_models_of_type(flexisv1.WorkPlanTask)
    required_tasks = [workplan_task.task_id for workplan_task in workplan_tasks]

    relevant_process_times = [process_time for process_time in relevant_process_times if process_time.task_id in required_tasks]
    relevant_setup_times = [setup_time for setup_time in relevant_setup_times if setup_time.task_from_id in required_tasks or setup_time.task_to_id in required_tasks]

    if resource.type_id == "resource_type_2":
        resource_modules = create_modules_AAS(resource, flexis_data_model)
    else:
        resource_modules = []

    procedure_ids = [
        f"{process_time.task_id}_{process_time.id_short}_procedure"
        for process_time in relevant_process_times
    ]
    procedure_ids += [
        f"{resource.id_short}_{availibility.id_short}_breakdown_procedure"
        for availibility in relevant_availibility
    ]
    procedure_ids += [
        f"{resource.id_short}_{availibility.id_short}_maintenance_procedure"
        for availibility in relevant_availibility
    ]
    procedure_ids += [
        f"{setup_time.resource_id}_{setup_time.id_short}_setup_procedure"
        for setup_time in relevant_setup_times
    ]
    if resource.type_id == "resource_type_4":
        procedure_ids += ["transport_procedure"]

    if not procedure_ids:
        resource_capabilities = None
        resource_control_logic = None
    else:
        resource_capabilities = resources.Capabilities(
            id=f"{resource.id_short}_capabilities",
            description=f"Capabilties of resource {resource.id_short}",
            procedures_ids=procedure_ids,
        )
        resource_control_logic = resources.ControlLogic(
            id=f"{resource.id_short}_control_logic",
            description=f"Control logic of resource {resource.id_short} with name {resource.name}",
            sequencing_policy="FIFO",
        )
        
    
    resource_general_information = create_resource_information(resource)
    if not relevant_variants:
        construction_data = None
    else:
        resource_variant = relevant_variants.pop()
        construction_data = resources.ConstructionData(
            id=f"{resource.id_short}_construction_data",
            description=f"Construction data of resource {resource.id_short} with name {resource.name}",
            cad_file=resource_variant.cad_file_name
        )

    resource_configuration = create_resource_configuration(resource, flexis_data_model)
    resource = resources.Resource(
        id=f"{resource.id_short}_resource",
        description=f"Resource with id {resource.id_short} and name {resource.name}",
        resource_information=resource_general_information,
        capabilities=resource_capabilities,
        control_logic=resource_control_logic,
        construction_data=construction_data,
        resource_configuration=resource_configuration,
    )
    return resource_modules + [resource]


def get_process_times_by_capability(resource: flexisv1.Resource, flexis_data_model: DataModel) -> Dict[str, List[flexisv1.ProcessTime]]:
    relevant_process_times = flexis_data_model.get_referencing_models_of_type(resource, flexisv1.ProcessTime)
    workplan_tasks = flexis_data_model.get_models_of_type(flexisv1.WorkPlanTask)
    required_tasks = [workplan_task.task_id for workplan_task in workplan_tasks]
    relevant_process_times = [process_time for process_time in relevant_process_times if process_time.task_id in required_tasks]
    process_times_by_capability = {}
    for process_time in relevant_process_times:
        task = flexis_data_model.get_model(process_time.task_id)
        if not task.name[8:] in process_times_by_capability:
            process_times_by_capability[task.name[8:]] = [process_time]
        else:
            process_times_by_capability[task.name[8:]].append(process_time)
    return process_times_by_capability

def create_modules_AAS(resource: flexisv1.Resource, flexis_data_model: DataModel) -> List[resources.Resource]:
    process_times_by_capability = get_process_times_by_capability(resource, flexis_data_model)

    modules = []
    for capability, process_times in process_times_by_capability.items():
        procedure_ids = [
            f"{process_time.task_id}_{process_time.id_short}_procedure"
            for process_time in process_times
        ]
        resource_capabilities = resources.Capabilities(
            id=f"{resource.id_short}_module_{capability}_capabilities",
            description=f"Capabilties of resource {resource.id_short}",
            procedures_ids=procedure_ids,
        )
        modules.append(
            resources.Resource(
                id=f"{resource.id_short}_module_{capability}",
                description=f"Module of resource {resource.id_short} with capability {capability}",
                resource_information=resources.ResourceInformation(
                    id=f"{resource.id_short}_module_{capability}_resource_information",
                    description=f"Resource information of module of resource {resource.id_short} with capability {capability}",
                    manufacturer="Bosch",
                    production_level="Module",
                    resource_type="Manufacturing",
                ),
                capabilities=resource_capabilities,
            )
        )
    return modules

def transform_orders(flexis_data_model: DataModel) -> List[order.Order]:
    order_data = flexis_data_model.get_models_of_type(flexisv1.Job)
    orders = [create_order_AAS(order) for order in order_data]
    return orders

def create_order_AAS(input_order: flexisv1.Job) -> order.Order:
    return order.Order(
        id=f"{input_order.id_short}_order",
        description=f"Order with id {input_order.id_short}.",
        product_id=f"{input_order.work_plan_id}_product",
        general_information=order.GeneralInformation(
            id=f"{input_order.id_short}_order_general_information",
            description=f"General information of order with id {input_order.id_short}.",
            quantity=1,
            order_id=input_order.id_short,
            priority=1,
            customer_information="OEM"
        ),
        order_schedule=order.OrderSchedule(
            id=f"{input_order.id_short}_order_schedule",
            description=f"Order schedule of order with id {input_order.id_short}.",
            release_time=input_order.release_date,
            due_time=input_order.due_date,
            target_time=input_order.due_date,
        ),
        ordered_products=order.OrderedProducts(
            id=f"{input_order.id_short}_ordered_products",
            description=f"Ordered products of order with id {input_order.id_short}.",
            ordered_products=[
                order.OrderedProduct(
                    id_short=f"{input_order.id_short}_ordered_product",
                    description=f"Ordered product of order with id {input_order.id_short}.",
                    product_type=f"{input_order.work_plan_id}_product",
                    target_quantity=1,
                    product_ids=[],
                )
            ],
        ),
    )

def transform_scenario(flexis_data_model: DataModel) -> List[change_scenario.ChangeScenario]:
    scenario_data = flexis_data_model.get_models_of_type(flexisv1.Scenario)
    scenarios = [create_scenario_AAS(scenario) for scenario in scenario_data]
    return scenarios

def create_scenario_AAS(input_scenario: flexisv1.Scenario) -> change_scenario.ChangeScenario:
    return change_scenario.ChangeScenario(
        id=f"{input_scenario.id_short}_scenario",
        description=f"Scenario with id {input_scenario.id_short}.",
        scenario_resources=change_scenario.ScenarioResources(
            id=f"{input_scenario.id_short}_scenario_resources",
            description=f"Resources of scenario with id {input_scenario.id_short}.",
            base_id=f"{input_scenario.resource_id}_resource",
        ),
        reconfiguration_constraints=change_scenario.ReconfigurationConstraints(
            id=f"{input_scenario.id_short}_reconfiguration_constraints",
            description=f"Reconfiguration constraints of scenario with id {input_scenario.id_short}.",
            max_reconfiguration_cost=input_scenario.max_reconfiguration_cost,
            max_number_of_machines=input_scenario.max_number_of_machines,
            max_number_of_transport_resources=input_scenario.max_number_of_transport_resources,
            max_reconfiguration_time=-1,
            max_number_of_process_modules_per_resource=input_scenario.max_number_of_process_modules_per_resource,
        ),
        reconfiguration_options=change_scenario.ReconfigurationOptions(
            id=f"{input_scenario.id_short}_reconfiguration_options",
            description=f"Reconfiguration options of scenario with id {input_scenario.id_short}.",
            reconfiguration_type="full",
            machine_controllers=["FIFO", "LIFO", "SPT"],
            transport_controllers=["FIFO", "SPT_transport"],
            routing_heuristics=["shortest_queue", "random"],
        ),
        reconfiguration_objectives=change_scenario.ReconfigurationObjectives(
            id=f"{input_scenario.id_short}_reconfiguration_objectives",
            description=f"Reconfiguration objectives of scenario with id {input_scenario.id_short}.",
            objectives=[
                change_scenario.Objective(
                    id_short=f"{input_scenario.id_short}_reconfiguration_objective_1",
                    description=f"Reconfiguration objective of scenario with id {input_scenario.id_short}.",
                    type="cost",
                    weight=0.1,
                ),
                change_scenario.Objective(
                    id_short=f"{input_scenario.id_short}_reconfiguration_objective_2",
                    description=f"Reconfiguration objective of scenario with id {input_scenario.id_short}.",
                    type="throughput",
                    weight=1000,
                ),
                change_scenario.Objective(
                    id_short=f"{input_scenario.id_short}_reconfiguration_objective_3",
                    description=f"Reconfiguration objective of scenario with id {input_scenario.id_short}.",
                    type="WIP",
                    weight=10,
                ),
            ],
        ),
    )