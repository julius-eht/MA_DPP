from sqlite3 import Date
from typing import Any, Dict, List, Annotated, Optional
import json
import pathlib
import uuid
import asyncio
import aiohttp


from fastapi import APIRouter, HTTPException, Body

from aas2openapi.models.base import Referable, AAS

import prodsys
from prodsys.optimization import evolutionary_algorithm_optimization, evolutionary_algorithm
from pydantic import BaseModel
from sdm.adapters.reference_model_adapters import prodsys_adapter


from sdm.model_core.data_model import NESTED_DICT
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models.pole_housing import PoleHousing
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models.training import Training
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models.webhook import Webhook
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models.webhook_events_item import WebhookEventsItem
from sdm.models.prodsys.prodsys import ProdsysModel
from sdm.models.sdm_reference_model import order
from sdm.models.sdm_reference_model.performance import Performance
from sdm.models.sdm_reference_model.procedure import Event
from sdm.models.sdm_reference_model.change_scenario import ChangeScenario
from sdm.models.sdm_reference_model.reference_model import ReferenceModel
from sdm.adapters.prodsys_adapters import reference_model_adapter
from sdm.adapters.simplan_adapters import (
    reference_model_adapter as RefModelToSimPlanAdapter,
)

from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.client import Client
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.process_data_controller import get_all_process_data
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.work_station_controller import get_all_work_stations
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.production_line_controller import get_all_production_lines
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.work_process_controller import get_all_work_processes
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.order_controller import get_all_orders

from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models import process_data, work_station, work_process, production_line, order


from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models import process_data
from sdm.models.morpheus.morpheus import MorpheusModel
from sdm.adapters.reference_model_adapters import morpheus_adapter
from aas2openapi.client import aas_client

router = APIRouter(
    prefix="/sdm_workflows",
    tags=["Workflows for SDM"],
    responses={404: {"description": "Not found"}},
)



# TODO: create requests for worklows in n8n:
# 1. GET reference model data -> read from file
# 2. map reference model to prodsys -> POST
# 3. POST optimize production system 
# 4. POST save configuration
# 5. POST schedule with flexis
# 6. POST save schedule
# 7. POST simulate with simplan
# 8. POST save as new productive configuration and plan


def get_use_case_reference_model_path() -> str:
    dir_path = pathlib.Path(__file__).parent.parent.absolute()
    file_path = dir_path / "example_data" / "reference_model_data.json"
    return str(file_path)

@router.get(
    "/get_reference_model_data",
    response_model=Dict[str, List[Any]],
    responses={
        200: {
            "description": "Sucessfully returned reference model data",
        },
        404: {"description": "No reference model data found"},
    }
)
async def get_reference_model_data():
    file_path = get_use_case_reference_model_path()
    with open(file_path, "r") as file:
        data = json.load(file)

    reference_model = ReferenceModel.from_dict(data)
    return reference_model.dict()



@router.post(
    "/map_reference_model_to_prodsys",
    response_model=prodsys.adapters.JsonProductionSystemAdapter,
    responses={
        200: {
            "description": "Sucessfully mapped reference model to prodsys",
        },
        404: {"description": "No reference model data found"},
    }
)
async def map_reference_model_to_prodsys(reference_model_data: Dict[str, List[Any]]) -> prodsys.adapters.JsonProductionSystemAdapter:
    reference_model = ReferenceModel.from_dict(reference_model_data)
    prodsys_model = reference_model_adapter.transform_reference_model(reference_model)
    return prodsys_model

@router.post(
    "/optimize_production_system",
    response_model=prodsys.adapters.JsonProductionSystemAdapter,
    responses={
        200: {
            "description": "Sucessfully optimized production system",
        },
        404: {"description": "No production system data found"},
    }
)
async def optimize_production_system(prodsys_model: prodsys.adapters.JsonProductionSystemAdapter) -> prodsys.adapters.JsonProductionSystemAdapter:
    hyper_parameters = evolutionary_algorithm.EvolutionaryAlgorithmHyperparameters(
        seed=0,
        number_of_generations=1,
        population_size=8,
        mutation_rate=0.2,
        crossover_rate=0.1,
        number_of_processes=1,
    )
    results_folder = pathlib.Path(__file__).parent.parent.absolute() / "example_data" / "optimization_results"
    evolutionary_algorithm_optimization(
        base_configuration=prodsys_model,
        hyper_parameters=hyper_parameters,
        save_folder=str(results_folder),
    )
    optimization_results_file_path = results_folder / "optimization_results.json"
    with open(optimization_results_file_path, "r") as file:
        optimization_results = json.load(file)
    best_individual_id = None
    generation_of_best_individual = None
    best_output = 0
    for generation, generation_results in optimization_results.items():
        for individual_id, individual_result in generation_results.items():
            if individual_result["fitness"][1] > best_output:
                best_individual_id = individual_id
                best_output = individual_result["fitness"][1]
                generation_of_best_individual = generation

    best_individual_file_path = results_folder / f"generation_{generation_of_best_individual}_{best_individual_id}.json"  
    print("best individual at:", best_individual_file_path)
    new_solution = prodsys.adapters.JsonProductionSystemAdapter()
    new_solution.read_data(file_path=best_individual_file_path)  
    new_solution.ID = f"ProductionSystem_{str(uuid.uuid1())}"
    # clean results folder
    for file in results_folder.glob("*.json"):
        file.unlink()
    return new_solution


@router.post(
    "/save_prodsys_configuration_to_aas_server",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Sucessfully saved configuration",
        },
        404: {"description": "No production system data found"},
    }
)
async def save_configuration(prodsys_model: prodsys.adapters.JsonProductionSystemAdapter) -> str:
    # TODO: delete demo mode
    return {"result": f"Sucessfully saved configuration {prodsys_model.ID}"}
    # TODO: also implement here the post with aas2openapi



@router.post(
        "/map_prodsys_to_reference_model",
        response_model=Dict[str, List[Any]],
        responses={
            200: {
                "description": "Sucessfully mapped prodsys to reference model",
            },
            404: {"description": "No production system data found"},
        }
)
async def map_prodsys_to_reference_model(prodsys_model: prodsys.adapters.JsonProductionSystemAdapter) -> Dict[str, List[Any]]:
    rnr = prodsys.runner.Runner(adapter=prodsys_model)
    rnr.initialize_simulation()
    rnr.run(7*24*60) # 7 days simulation in minutes
    performance = rnr.get_performance_data()
    prodsys_data_model = ProdsysModel(performance, adapter=prodsys_model)
    reference_model = prodsys_adapter.transform_prodsys_model(prodsys_data_model)
    return reference_model.dict()


@router.post(
    "/schedule_with_flexis",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Sucessfully scheduled",
        },
        404: {"description": "No production system data found"},
    }
)
async def schedule_with_flexis(reference_model: Dict[str, List[Any]]) -> str:
    if not reference_model:
        # TODO: delete demo mode
        await asyncio.sleep(5)
        return {"result": f"Scheduling is feasible. Sucessfully created schedule."}
   # TODO: make mapping, create schedule with flexis and return schedule (and not info)


@router.post(
    "/save_schedule_to_aas_server",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Sucessfully saved schedule",
        },
        404: {"description": "No production system data found"},
    }
)
async def save_schedule_to_aas_server(schedule: List[Event]) -> Dict[str, str]:
    if not schedule:
        # TODO: delete demo mode
        return {"result": f"Sucessfully saved schedule"}
    # TODO: make put requests to aas server that updates the correct events of the procedure



@router.post(
    "/simulate_with_simplan",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Sucessfully simulated",
        },
        404: {"description": "No production system data found"},
    }
)
async def simulate_with_simplan(reference_model_data: Dict[str, List[Any]]) -> Dict[str, str]:
    if not reference_model_data:
        # TODO: delete demo mode
        await asyncio.sleep(5)
        return {"result": "No production system data found"}
    reference_model = ReferenceModel.from_dict(reference_model_data)
    simplan_model = RefModelToSimPlanAdapter.transform_reference_model(reference_model)
    # TODO: make request for simulation and return performance

@router.post(
    "/adjust_optimization_parameters",
    response_model=Dict[str, List[Any] | None],
    responses={
        200: {
            "description": "Sucessfully saved new productive configuration and plan",
        },
        404: {"description": "No production system data found"},
    }
)
async def adjust_optimization_parameters(reference_model_data: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
    reference_model = ReferenceModel.from_dict(reference_model_data)
    scenario: ChangeScenario = reference_model.get_models_of_type(ChangeScenario).pop()
    scenario.reconfiguration_constraints.max_number_of_machines += 1
    scenario.reconfiguration_constraints.max_number_of_transport_resources += 1
    scenario.reconfiguration_constraints.max_reconfiguration_cost += 250000
    if scenario.reconfiguration_constraints.max_reconfiguration_cost > 500000:
        return None
    return reference_model.dict()


@router.post(
    "/kenbun_breakdown_monitoring",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Monitoring detected required reschuedling of production",
        },
        404: {"description": "No production system data found"},
    }
)
async def kenbun_breakdown_monitoring(monitoring_data: Dict[str, str]) -> Dict[str, str]:
    # TODO: delete demo mode
    if monitoring_data["status"] == "BREAKDOWN":
        return {"result": "Monitoring detected required reschuedling of production", "scheduling_required": "True"}
    return {"result": "Monitoring detected no required reschuedling of production", "scheduling_required": "False"}
    # TODO: real implementation of kenbun services

