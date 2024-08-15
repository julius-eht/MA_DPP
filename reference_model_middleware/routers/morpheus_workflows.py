import datetime
from typing import Dict, List, Optional
import json
import aiohttp
import os
from fastapi import APIRouter, HTTPException

from aas2openapi.models.base import Referable

from pydantic import BaseModel



from sdm.models import morpheus
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models.editable_variant import EditableVariant
from sdm.models.sdm_reference_model import order, procedure
from sdm.models.sdm_reference_model.performance import Performance
from sdm.models.sdm_reference_model.reference_model import ReferenceModel

from sdm.models.morpheus.morpheus import MorpheusModel
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.client import Client

from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models import (
    editable_part,
    game_round,
    part,
    training,
    variant,
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models.pole_housing import (
    PoleHousing,
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models.training import (
    Training,
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models.webhook import (
    Webhook,
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models.webhook_events_item import (
    WebhookEventsItem,
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models import (
    process_data,
    work_station,
    work_process,
    production_line,
    order,
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models import (
    process_data,
)

from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.training_controller import (
    get_running_training,
    get_all_trainings,
)

from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.pole_housing_controller import (
    get_all_pole_housing
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.webhook_controller import (
    add_webhook,
)

from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.game_round_controller import (
    get_running_game_round,
    get_all_game_rounds,
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.editable_part_controller import (
    get_all_editable_parts_in_active_training,
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.editable_variant_controller import (
    get_all_editable_variants_in_training,
)

from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.process_data_controller import (
    get_all_process_data,
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.work_station_controller import (
    get_all_work_stations,
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.production_line_controller import (
    get_all_production_lines,
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.work_process_controller import (
    get_all_work_processes,
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.api.order_controller import (
    get_all_orders,
)


from sdm.adapters.reference_model_adapters import morpheus_adapter
from aas2openapi.client import aas_client

router = APIRouter(
    prefix="/moprheus_workflows",
    tags=["Workflows for Morpheus"],
    responses={404: {"description": "Not found"}},
)

EVENT_LOG_BUCKET = "learning_factory_mes_event_data" # done
EVENT_GAME_ROUND_TRAINING_BUCKET = "event_game_round_training" # done
WORKSTATION_PRODUCTION_LINE_ASSOCIATION_BUCKET = "production_line_workstations"
WORKPROCESS_VARIANT_ASSOCIATION_BUCKET = "variant_workprocesses"
POLEHOUSING_VARIANT_ASSOCIATION_BUCKET = "polehousing_variant"


 
DATENBERG_URL = (
    "https://api.datenberg.eu/v1-put-json?key=f5305dbdd353422583586ac39e208eef&bucket="
)
MES_URL = "http://localhost:8080"


async def get_process_data_from_mes(mes_url: str) -> List[process_data.ProcessData]:
    client = Client(mes_url)
    try:
        process_data_response = await get_all_process_data.asyncio_detailed(
            client=client
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot connect to MES server at {mes_url} for querying process data because of error: {e}",
        )
    if not process_data_response.status_code == 200:
        raise HTTPException(
            status_code=process_data_response.status_code,
            detail=process_data_response.content,
        )
    process_data_dict = json.loads(process_data_response.content)
    return [
        process_data.ProcessData.from_dict(process_data_instance)
        for process_data_instance in process_data_dict
    ]


async def get_work_processes_from_mes(mes_url: str) -> List[work_process.WorkProcess]:
    client = Client(mes_url)
    try:
        work_process_response = await get_all_work_processes.asyncio_detailed(
            client=client
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot connect to MES server at {mes_url} for querying work processes because of error: {e}",
        )
    if not work_process_response.status_code == 200:
        raise HTTPException(
            status_code=work_process_response.status_code,
            detail=work_process_response.content,
        )
    work_process_dict = json.loads(work_process_response.content)
    return [
        work_process.WorkProcess.from_dict(work_process_instance)
        for work_process_instance in work_process_dict
    ]


async def get_work_stations_from_mes(mes_url) -> List[work_station.WorkStation]:
    client = Client(mes_url)
    try:
        work_station_response = await get_all_work_stations.asyncio_detailed(
            client=client
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot connect to MES server at {mes_url} for querying work stations because of error: {e}",
        )
    if not work_station_response.status_code == 200:
        raise HTTPException(
            status_code=work_station_response.status_code,
            detail=work_station_response.content,
        )
    work_station_dict = json.loads(work_station_response.content)
    # replace workstation status
    for instance in work_station_dict:
        if instance["workStationStatus"]:
            continue
        del instance["workStationStatus"]
    return [
        work_station.WorkStation.from_dict(work_station_instance)
        for work_station_instance in work_station_dict
    ]


async def get_production_lines_from_mes(
    mes_url,
) -> List[production_line.ProductionLine]:
    client = Client(mes_url)
    try:
        production_line_response = await get_all_production_lines.asyncio_detailed(
            client=client
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot connect to MES server at {mes_url} for querying production lines because of error: {e}",
        )
    if not production_line_response.status_code == 200:
        raise HTTPException(
            status_code=production_line_response.status_code,
            detail=production_line_response.content,
        )
    production_line_dict = json.loads(production_line_response.content)
    return [
        production_line.ProductionLine.from_dict(production_line_instance)
        for production_line_instance in production_line_dict
    ]


async def get_all_orders_from_mes(mes_url) -> List[order.Order]:
    client = Client(mes_url)
    try:
        order_response = await get_all_orders.asyncio_detailed(client=client)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot connect to MES server at {mes_url} for querying orders because of error: {e}",
        )
    if not order_response.status_code == 200:
        raise HTTPException(
            status_code=order_response.status_code, detail=order_response.content
        )
    order_dict = json.loads(order_response.content)
    for instance in order_dict:
        keys_to_delete = []
        for key in instance:
            if instance[key]:
                continue
            keys_to_delete.append(key)
        for key in keys_to_delete:
            del instance[key]
    return [order.Order.from_dict(order_instance) for order_instance in order_dict]


async def get_all_game_rounds_from_mes(mes_url) -> List[game_round.GameRound]:
    client = Client(mes_url)
    try:
        game_rounds_response = await get_all_game_rounds.asyncio_detailed(client=client)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot connect to MES server at {mes_url} for querying game rounds because of error: {e}",
        )
    if not game_rounds_response.status_code == 200:
        raise HTTPException(
            status_code=game_rounds_response.status_code,
            detail=game_rounds_response.content,
        )
    game_round_dict = json.loads(game_rounds_response.content)
    # for instance in game_round_dict:
    #     keys_to_delete = []
    #     for key in instance:
    #         if instance[key]:
    #             continue
    #         keys_to_delete.append(key)
    #     for key in keys_to_delete:
    #         del instance[key]
    return [
        game_round.GameRound.from_dict(order_instance)
        for order_instance in game_round_dict
    ]

async def get_all_trainings_from_mes(mes_url) -> List[training.Training]:
    client = Client(mes_url)
    try:
        training_response = await get_all_trainings.asyncio_detailed(client=client)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot connect to MES server at {mes_url} for querying trainings because of error: {e}",
        )
    if not training_response.status_code == 200:
        raise HTTPException(
            status_code=training_response.status_code,
            detail=training_response.content,
        )
    training_dict = json.loads(training_response.content)
    # for instance in game_round_dict:
    #     keys_to_delete = []
    #     for key in instance:
    #         if instance[key]:
    #             continue
    #         keys_to_delete.append(key)
    #     for key in keys_to_delete:
    #         del instance[key]
    return [
        training.Training.from_dict(order_instance)
        for order_instance in training_dict
    ]

async def get_all_parts_from_mes(mes_url) -> List[editable_part.EditablePart]:
    client = Client(mes_url)
    try:
        part_response = await get_all_editable_parts_in_active_training.asyncio_detailed(client=client)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot connect to MES server at {mes_url} for querying parts because of error: {e}",
        )
    if not part_response.status_code == 200:
        raise HTTPException(
            status_code=part_response.status_code, detail=part_response.content
        )
    part_dict = json.loads(part_response.content)
    return [editable_part.EditablePart.from_dict(part_instance) for part_instance in part_dict]

async def get_all_variants_from_mes(mes_url) -> List[EditableVariant]:
    client = Client(mes_url)
    try:
        variant_response = await get_all_editable_variants_in_training.asyncio_detailed(client=client)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot connect to MES server at {mes_url} for querying variants because of error: {e}",
        )
    if not variant_response.status_code == 200:
        raise HTTPException(
            status_code=variant_response.status_code, detail=variant_response.content
        )
    variant_dict = json.loads(variant_response.content)
    return [EditableVariant.from_dict(variant_instance) for variant_instance in variant_dict]


async def get_all_pole_housings_from_mes(mes_url) -> List[PoleHousing]:
    client = Client(mes_url)
    try:
        pole_housing_response = await get_all_pole_housing.asyncio_detailed(
            client=client
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot connect to MES server at {mes_url} for querying pole housings because of error: {e}",
        )
    if not pole_housing_response.status_code == 200:
        raise HTTPException(
            status_code=pole_housing_response.status_code,
            detail=pole_housing_response.content,
        )
    pole_housing_dict = json.loads(pole_housing_response.content)
    return [
        PoleHousing.from_dict(pole_housing_instance)
        for pole_housing_instance in pole_housing_dict
    ]

async def get_running_game_round_from_mes(mes_url) -> game_round.GameRound:
    client = Client(mes_url)
    try:
        game_round_response = await get_running_game_round.asyncio_detailed(
            client=client
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot connect to MES server at {mes_url} for querying running game round because of error: {e}",
        )
    if not game_round_response.status_code == 200:
        raise HTTPException(
            status_code=game_round_response.status_code,
            detail=game_round_response.content,
        )
    return game_round.GameRound.from_dict(json.loads(game_round_response.content))

async def get_running_training_from_mes(mes_url) -> training.Training:
    client = Client(mes_url)
    try:
        training_response = await get_running_training.asyncio_detailed(
            client=client
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cannot connect to MES server at {mes_url} for querying running training because of error: {e}",
        )
    if not training_response.status_code == 200:
        raise HTTPException(
            status_code=training_response.status_code,
            detail=training_response.content,
        )
    return training.Training.from_dict(json.loads(training_response.content))


async def get_morpheus_model_from_mes(mes_url: str) -> MorpheusModel:
    part_list = await get_all_parts_from_mes(mes_url=mes_url)
    work_process_list = await get_work_processes_from_mes(mes_url=mes_url)
    variant_list = await get_all_variants_from_mes(mes_url=mes_url)
    work_station_list = await get_work_stations_from_mes(mes_url=mes_url)
    production_line_list = await get_production_lines_from_mes(mes_url=mes_url)
    process_data_list = await get_process_data_from_mes(mes_url=mes_url)
    order_list = await get_all_orders_from_mes(mes_url=mes_url)
    pole_housing_list = await get_all_pole_housings_from_mes(mes_url=mes_url)

    game_rounds_list = await get_all_game_rounds_from_mes(mes_url=mes_url)
    training_list = await get_all_trainings_from_mes(mes_url=mes_url)

    return MorpheusModel(
        *part_list,
        *work_process_list,
        *variant_list,
        *work_station_list,
        *production_line_list,
        *process_data_list,
        *order_list,
        *pole_housing_list,
        *game_rounds_list,
        *training_list
    )


async def save_reference_model_in_middleware(
    reference_model: ReferenceModel,
) -> Dict[str, str]:
    # with open("reference_model_data.json", "w") as f:
    #     f.write(reference_model.json())

    for models in reference_model.get_top_level_models().values():
        for model in models:
            if await aas_client.aas_is_on_server(model.id):
                aas_on_server: Referable = await aas_client.get_aas_from_server(
                    model.id
                )
                aas_on_server = model
                await aas_client.put_aas_to_server(aas_on_server)
            else:
                await aas_client.post_aas_to_server(model)

    return {"result": f"Sucessfully retrieved learning factory data"}


@router.post(
    "/activate_mes_event_data_webhook",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Sucessfully saved mes event data",
        },
        404: {"description": "No production system data found"},
    },
)
async def active_mes_event_data_webhook(
    webhook_host: str = "http://host.docker.internal:8000",
    mes_url: str = "http://localhost:8080",
) -> Dict[str, str]:
    os.environ["MES_URL"] = mes_url
    client = Client(mes_url)
    request_bodies = []
    request_bodies.append(
        Webhook(
            endpoint=webhook_host + "/moprheus_workflows/mes_event_data",
            events=[WebhookEventsItem.FINISHED_PRODUCTION_PROCESS],
        )
    )
    request_bodies.append(
        Webhook(
            endpoint=webhook_host + "/moprheus_workflows/training_started",
            events=[WebhookEventsItem.START_TRAINING],
        )
    )
    request_bodies.append(
        Webhook(
            endpoint=webhook_host
            + "/moprheus_workflows/pole_housing_matched",
            events=[WebhookEventsItem.POLE_HOUSING_MATCHED_TO_ORDER],
        )
    )
    request_bodies.append(
        Webhook(
            endpoint=webhook_host
            + "/moprheus_workflows/pole_housing_entered_production",
            events=[WebhookEventsItem.POLE_HOUSING_ENTERED_PRODUCTION],
        )
    )
    request_bodies.append(
        Webhook(
            endpoint=webhook_host
            + "/moprheus_workflows/pole_housing_finisheded_production",
            events=[WebhookEventsItem.POLE_HOUSING_FINISHED_PRODUCTION],
        )
    )
    for request_body in request_bodies:
        try:
            response = await add_webhook.asyncio_detailed(
                client=client, json_body=request_body
            )
            print(response.status_code, response.content)
            if not response.status_code == 200:
                raise HTTPException(
                    status_code=response.status_code, detail=response.content
                )
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"Cannot connect to MES server at {mes_url} with error code: {e}",
            )
    return {
        "result": f"Succesfully sent webhook requests for {webhook_host} to {mes_url}"
    }


async def handle_workstation_production_line_association(morpheus_model: MorpheusModel):
    for production_line_instance in morpheus_model.production_lines:
        for work_station_id in production_line_instance.work_station_ids:
            work_station_instance: work_station.WorkStation = morpheus_model.get_model(work_station_id)
            if not work_station_instance:
                continue
            production_line_work_station_data = {
                    "production_line_id": production_line_instance.id,
                    "production_line_name": production_line_instance.name,
                    "work_station_id": "resource_" + work_station_instance.id,
                    "work_station_name": work_station_instance.name,
                }
            await send_data_to_datenberg_bucket(
                WORKSTATION_PRODUCTION_LINE_ASSOCIATION_BUCKET, json.dumps(production_line_work_station_data)
            )


async def handle_workprocess_variant_association(morppheus_model: MorpheusModel):
    for variant in morppheus_model.variants:
        for counter, work_process_id in enumerate(variant.work_process_sequence_ids):
            work_process_instance: work_process.WorkProcess = morppheus_model.get_model(work_process_id)
            if not work_process_instance:
                continue
            variant_work_process_data = {
                "variant_id": variant.id,
                "variant_name": variant.name,
                "work_process_id": "procedure_" + work_process_instance.id,
                "work_process_name": work_process_instance.name,
                "sequence_number": counter,
            }
            await send_data_to_datenberg_bucket(
                WORKPROCESS_VARIANT_ASSOCIATION_BUCKET, json.dumps(variant_work_process_data)
            )


async def handle_datenberg_training_started_data(morpheus_model: MorpheusModel):
    await handle_workstation_production_line_association(morpheus_model)
    await handle_workprocess_variant_association(morpheus_model)


@router.post(
    "/training_started",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Sucessfully considered starting of training.",
        },
        404: {"description": "No production system data found"},
    },
)
async def training_started(training: dict) -> Dict[str, str]:
    mes_url = os.environ.get("MES_URL")
    if not mes_url:
        raise HTTPException(
            status_code=404,
            detail="No MES URL found in environment variables",
        )
    morpheus_model = await get_morpheus_model_from_mes(mes_url=os.environ.get("MES_URL"))
    await handle_datenberg_training_started_data(morpheus_model)
    # TODO: maybe also send data to AAS server for product passport information!
    return {"result": f"Succesfully considered training started event."}


async def handle_datenberg_polehousing_matched_data(pole_housing: PoleHousing):
    pole_housing_order_data = {
        "product_id": "product_" + pole_housing.id,
        "variant_id": pole_housing.variant_id,
    }
    await send_data_to_datenberg_bucket(
        POLEHOUSING_VARIANT_ASSOCIATION_BUCKET, json.dumps(pole_housing_order_data)
    )

@router.post(
    "/pole_housing_matched",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Sucessfully considered polehousing matched to order.",
        },
        404: {"description": "No production system is found"},
    },
)
async def polehousing_matched(pole_housing: dict) -> Dict[str, str]:
    pole_housing_object = PoleHousing.from_dict(pole_housing)
    await handle_datenberg_polehousing_matched_data(pole_housing_object)
    # TODO: also update for product passport here the product type and order data
    return {"result": f"Succesfully considered polehousing matched to order."}

def get_mes_url():
    mes_url = os.environ.get("MES_URL")
    if not mes_url:
        raise HTTPException(
            status_code=404,
            detail="No MES URL found in environment variables. Please set MES_URL by activating the webhook.",
        )
    return mes_url

@router.post(
    "/pole_housing_entered_production",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Sucessfully considered polehousing entered production.",
        },
        404: {"description": "No production system is found"},
    },
)
async def polehousing_entered_production(
    pole_housing: dict
) -> Dict[str, str]:
    pole_housing_object = PoleHousing.from_dict(pole_housing)
    procedure_instance = procedure.Event(
        id_short="starting_production_" + pole_housing_object.id,
        time=datetime.datetime.now(datetime.UTC).isoformat(),
        resource_id="",
        procedure_id="", 
        procedure_type= procedure.ProcedureTypeEnum.ORDER_RELEASE,
        activity= procedure.ActivityTypeEnum.START, 
        product_id="product_" + pole_housing_object.id, 
        success=True
    )
    await send_data_to_datenberg_bucket(EVENT_LOG_BUCKET, procedure_instance.json())
    await send_event_game_round_training_to_datenberg_bucket(get_mes_url(), procedure_instance)
    return {"result": f"Succesfully considered polehousing entered production."}


@router.post(
    "/pole_housing_finished_production",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Sucessfully considered polehousing finished production.",
        },
        404: {"description": "No production system is found"},
    },
)
async def polehousing_finished_production(
    pole_housing: dict
) -> Dict[str, str]:
    pole_housing_object = PoleHousing.from_dict(pole_housing)
    procedure_instance = procedure.Event(
        id_short="finished_production_" + pole_housing_object.id,
        time=datetime.datetime.now(datetime.UTC).isoformat(),
        resource_id="",
        procedure_id="", 
        procedure_type= procedure.ProcedureTypeEnum.ORDER_SHIPPING,
        activity= procedure.ActivityTypeEnum.START, 
        product_id="product_" + pole_housing_object.id, 
        success=True
    )
    await send_data_to_datenberg_bucket(EVENT_LOG_BUCKET, procedure_instance.json())
    await send_event_game_round_training_to_datenberg_bucket(get_mes_url(), procedure_instance)
    return {"result": f"Succesfully considered polehousing finished production."}


async def send_data_to_datenberg_bucket(bucket: str, data: str):
    datenberg_bucket_url = DATENBERG_URL + bucket
    async with aiohttp.ClientSession() as session:
        print(f"Sending data to datenberg bucket {datenberg_bucket_url} with data: \n {data}")
        async with session.post(url=datenberg_bucket_url, data=data) as response:
            if not response.status == 200:
                raise HTTPException(
                    status_code=response.status, detail=await response.text()
                )

async def send_event_game_round_training_to_datenberg_bucket(mes_url: str, event: procedure.Event):
    running_training = await get_running_training_from_mes(mes_url)
    running_game_round = await get_running_game_round_from_mes(mes_url)
    event_game_round_data = {
                "training_id": running_training.id,
                "training_name": running_training.name,
                "game_round_id": running_game_round.id,
                "game_round_name": running_game_round.name,
                "event_id": event.id_short,
            }
    await send_data_to_datenberg_bucket(EVENT_GAME_ROUND_TRAINING_BUCKET, json.dumps(event_game_round_data))

async def handle_datenberg_event_data(performance_aas_list: List[Performance]):
    mes_url = get_mes_url()
    for performance_aas_instance in performance_aas_list:
        for event in performance_aas_instance.event_log.event_log:
            await send_data_to_datenberg_bucket(EVENT_LOG_BUCKET, event.json())
            await send_event_game_round_training_to_datenberg_bucket(mes_url, event)


async def handle_aas_event_data(performance_aas_list: List[Performance]):
    for performance_aas_instance in performance_aas_list:
        try:
            if await aas_client.aas_is_on_server(performance_aas_instance.id):
                aas_on_server: Performance = await aas_client.get_aas_from_server(
                    performance_aas_instance.id
                )
                aas_on_server.event_log.event_log += (
                    performance_aas_instance.event_log.event_log
                )
                await aas_client.put_aas_to_server(aas_on_server)
            else:
                await aas_client.post_aas_to_server(performance_aas_instance)
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"Cannot connect to AAS server at with error {e}",
            )


class ProcessData(BaseModel):
    id: str
    entryTime: str
    outputTime: Optional[str]
    workStationId: str
    workProcessId: str
    engineStatus: Optional[bool]
    atEntryPoint: Optional[bool]
    poleHousingId: str
    gameRoundId: str


@router.post(
    "/mes_event_data",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Sucessfully saved mes event data",
        },
        404: {"description": "No production system data found"},
    },
)
async def mes_event_data(mes_event_data: ProcessData) -> Dict[str, str]:
    process_data_client = process_data.ProcessData.from_dict(mes_event_data.dict())
    morpheus_model = MorpheusModel(process_data_client)
    performance_aas_list = morpheus_adapter.transform_performances(morpheus_model)
    await handle_datenberg_event_data(performance_aas_list=performance_aas_list)
    await handle_aas_event_data(performance_aas_list=performance_aas_list)
    return {
        "result": f"Sucessfully saved mes event data to performance aas' with ids: {[performance_aas_instance.id for performance_aas_instance in performance_aas_list]}"
    }



@router.post(
    "/mes_event_data_test_process_data_input",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Sucessfully saved mes event data",
        },
        404: {"description": "No production system data found"},
    },
)
async def mes_event_data(mes_event_data: ProcessData) -> Dict[str, str]:
    print(mes_event_data, type(mes_event_data))
    process_data_client = process_data.ProcessData.from_dict(mes_event_data.dict())
    morpheus_model = MorpheusModel(process_data_client)
    performance_aas_list = morpheus_adapter.transform_performances(morpheus_model)
    return {
        "result": f"Sucessfully saved mes event data to performance aas' with ids: {[performance_aas_instance.id for performance_aas_instance in performance_aas_list]}"
    }




@router.post(
    "/mes_event_data_test_body_input",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Sucessfully saved mes event data",
        },
        404: {"description": "No production system data found"},
    },
)
async def mes_event_data(mes_event_data: dict) -> Dict[str, str]:
    print(mes_event_data, type(mes_event_data))
    return {
        "result": f"Sucessfully accepted mes event data body: {mes_event_data}"
    }

@router.get(
    "/load_learning_factory_configuration_in_middleware",
    response_model=Dict[str, str],
    responses={
        200: {
            "description": "Sucessfully retrieved learning factory data",
        },
        404: {"description": "No production system data found"},
    },
)
async def load_learning_factory_configuration_in_middleware(
    mes_url: str = "http://localhost:8080",
) -> Dict[str, str]:
    morpheus_model = await get_morpheus_model_from_mes(mes_url=mes_url)
    reference_model = morpheus_adapter.transform_morpheus_to_reference_model(
        morpheus_model
    )
    return await save_reference_model_in_middleware(reference_model=reference_model)
