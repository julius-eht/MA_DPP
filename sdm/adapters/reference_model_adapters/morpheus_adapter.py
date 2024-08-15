from typing import List, Optional


from sdm.models.sdm_reference_model import ReferenceModel, processes, product, procedure, resources, order, distribution, change_scenario, performance
from sdm.models.morpheus.morpheus import MorpheusModel
from sdm.model_core.data_model import DataModel

from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models import order as mes_order
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models import production_line, work_station, process_data


def fix_name_for_id(name: str) -> str:
    return name.replace(" ", "").replace("(", "_").replace(")", "_")


def transform_morpheus_to_reference_model(morpheus_model: MorpheusModel) -> ReferenceModel:
    """
    Transform a MES moprheus data model to a reference model.

    Args:
        flexis_model (DataModel): _description_

    Returns:
        ReferenceModel: _description_
    """
    orders = transform_orders(morpheus_model)
    resources = transform_resources(morpheus_model)
    if "ProcessData" in morpheus_model._models_key_type:
        performances = transform_performances(morpheus_model)
    else:
        performances = []
    # TODO: implement adapter for product -> product (consider MES Variants and Parts) to get mapping of polehousing_id and product_id

    # product type, product instanz / product id, polehousing_id / rfid tag id

    return ReferenceModel(
        orders,
        resources,
        performances
    )

# TODO docstrings are missing

def transform_orders(morpheus_data_model: MorpheusModel) -> List[order.Order]:
    order_data = morpheus_data_model.get_models_of_type(model_type=mes_order.Order)
    orders = [create_order_AAS(order) for order in order_data]
    return orders


def create_order_AAS(input_order: mes_order.Order) -> order.Order:
    return order.Order(
        id="order_" + input_order.id,
        description=f"Order with id {input_order.id}.",
        general_information = order.GeneralInformation(
            id = f"order_{input_order.id}_information", 
            priority= input_order.priority_level if input_order.priority_level else 0,
            customer_information = "OEM",
            order_id=f"order_{input_order.id}_id_information"
        ), 
        order_schedule=order.OrderSchedule(
            id=f"order_{input_order.id}_order_schedule", 
            release_time = input_order.time_stamp.isoformat() if input_order.time_stamp else "",
            due_time=input_order.delivery_time.isoformat() if input_order.delivery_time else "",
            target_time=input_order.delivery_time.isoformat() if input_order.delivery_time else ""
        ),
        ordered_products=order.OrderedProducts(
            id=f"order_{input_order.id}_ordered_products",
            ordered_products= create_ordered_products(input_order)
        )
    )

def create_ordered_products(input_order: mes_order.Order) -> List[order.OrderedProduct]:
    product_ids = []
    if input_order.pole_housing_ids:
        product_ids = [f"product_{product_id}" for product_id in input_order.pole_housing_ids]
    return [
            order.OrderedProduct(
                id_short=f"order_{input_order.id}_ordered_product_{input_order.variant_id}", 
                product_type= input_order.variant_id,
                target_quantity=input_order.amount, 
                product_ids=product_ids
            )]
        


def transform_resources(morpheus_data_model: MorpheusModel) -> list[resources.Resource]:
    resource_data_work_station = morpheus_data_model.get_models_of_type(work_station.WorkStation)
    resource_data_production_line = morpheus_data_model.get_models_of_type(production_line.ProductionLine)

    resources = [create_resource_AAS_ws(resource, morpheus_data_model) for resource in resource_data_work_station] + [create_resource_AAS_pl(resource, morpheus_data_model) for resource in resource_data_production_line]
    return resources

def create_resource_AAS_ws(input_resource: work_station.WorkStation, morpheus_data_model: MorpheusModel) -> resources.Resource:
    input_resource.id = fix_name_for_id(input_resource.id)
    return resources.Resource(
        id="resource_" + input_resource.id,
        resource_information=resources.ResourceInformation(
            id = f"resource_{input_resource.id}_resource_information",
            manufacturer="Bosch",
            production_level="Station",
            resource_type="Manufacturing"
        ),
        capabilities=resources.Capabilities(
            id=f"resource_{input_resource.id}_id_capabilities", 
            procedures_ids=input_resource.work_process_ids
        ), 
        resource_performances=resources.ResourcePerformances(
            id = f"resource_{input_resource.id}id_resource_performances",
            resource_performance= create_resource_performance(morpheus_data_model)
        )    
    )

#transfer workstations -> procedures_ids = list of workstation ids
def create_resource_AAS_pl(input_resource: production_line.ProductionLine, morpheus_data_model: MorpheusModel) -> resources.Resource:
    input_resource.id = fix_name_for_id(input_resource.id)
    return resources.Resource(
        id="resource_" + input_resource.id,
        resource_information=resources.ResourceInformation(
            id = f"resource_{input_resource.id}_resource_information",
            manufacturer="Bosch",
            production_level="System",
            resource_type="Manufacturing"
        ),
        capabilities=resources.Capabilities(
            id = f"resource_{input_resource.id}_id_capabilities",
            procedures_ids=input_resource.work_station_ids
        ),
        resource_configuration=resources.ResourceConfiguration(
            id= f"resource_{input_resource.id}_id_configuration",
            sub_resources=create_subresources(input_resource)
        ),
        # Correct like this?
        resource_performances=resources.ResourcePerformances(
            id = f"resource_{input_resource.id}id_resource_performances",
            resource_performance= create_resource_performance(morpheus_data_model)
        )
    )

def create_resource_performance(morpheus_data_model: MorpheusModel) -> List[resources.ResourcePerformance]:
    if "ProcessData" not in morpheus_data_model._models_key_type:
        return []
    event_data: List[process_data.ProcessData] = morpheus_data_model.get_models_of_type(process_data.ProcessData)
    unique_gameround_ids = set()
    for event in event_data:
        unique_gameround_ids.add(event.game_round_id)
    unique_gameround_ids_list = list(unique_gameround_ids)

    list_resourceperformance = []

    for gameround_id in unique_gameround_ids_list:
        list_resourceperformance.append(resources.ResourcePerformance(
            id_short=f"gameround_{gameround_id}_resource_performance",
            obtained_performance_from="Morpheus_MES"      
            )
        
        )

def create_subresources(input_resource: production_line.ProductionLine) -> list[resources.SubResource]:
    sub_resources_list = []
    for subresource in input_resource.work_station_ids:
        subresource = fix_name_for_id(subresource)
        sub_resources_list.append(resources.SubResource(
            id_short=f"subresource_{subresource}_subresource", 
            resource_id=f"resource_{subresource}",
            # TODO update position and orientation if available
            position=[0,0], 
            orientation=[0] 
        ))
    
    return sub_resources_list

def transform_performances(morpheus_data_model: MorpheusModel) -> List[performance.Performance]:
    
    event_data: List[process_data.ProcessData] = morpheus_data_model.get_models_of_type(process_data.ProcessData)
    unique_gameround_ids = set()
    for event in event_data:
        unique_gameround_ids.add(event.game_round_id)
    unique_gameround_ids_list = list(unique_gameround_ids)

    list_performances = []

    for gameround_id in unique_gameround_ids_list:
        list_performances.append(performance.Performance(
            id=f"gameround_{gameround_id}_performance",
            key_performance_indicators=performance.KeyPerformanceIndicators(
                id=f"gameround_{gameround_id}_performance_kpi",
                kpis=[]
            ),
            event_log=performance.EventLog(
                id=f"gameround_{gameround_id}_performance_eventlog",
                event_log=transform_events(morpheus_data_model, gameround_id)
            )
        )
    )
    return list_performances

def transform_events(morpheus_data_model: MorpheusModel, gameround_id) -> List[procedure.Event]:
    process_data_objects: List[process_data.ProcessData] = morpheus_data_model.get_models_of_type(process_data.ProcessData)
    events = [create_AAS_event(process_data_instance) for process_data_instance in process_data_objects if process_data_instance.game_round_id==gameround_id]
    return events

def create_AAS_event(input_event: process_data.ProcessData) -> procedure.Event:
    return procedure.Event(
        id_short="event_" + input_event.id,
        time=input_event.entry_time.isoformat(),
        resource_id=f"resource_{fix_name_for_id(input_event.work_station_id)}",
        procedure_id=f"procedure_{fix_name_for_id(input_event.work_process_id)}", 
        procedure_type= procedure.ProcedureTypeEnum.PRODUCTION,
        activity= procedure.ActivityTypeEnum.START, 
        product_id="product_" + input_event.pole_housing_id, 
        actual_end_time=input_event.output_time.isoformat(),
        success=input_event.engine_status
    )