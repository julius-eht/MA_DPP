from typing import List, Type, TypeVar

import pandas as pd
from aas2openapi.util.convert_util import convert_camel_case_to_underscrore_str
from openpyxl import load_workbook
from pydantic import PrivateAttr
from sdm.model_core.data_model import ORIGIN_DATA_MODEL, REFERABLE_MODEL
from sdm.model_core.transform_model import AbstractTransformModel
from sdm.models.flexisv1 import flexisv1
from sdm.models.flexisv1.flexisv1 import FlexisDataModel
from sdm.models.flexisv1.util import FlexisDataFrames


def rearrange_string(input_str):
    parts = input_str.split("_")
    id_index = -1
    for counter, string in enumerate(parts):
        if string == "id" and not counter == len(parts) - 1:
            id_index = counter
            break
    if id_index == -1:
        return input_str
    parts.pop(id_index)
    parts.append("id")
    return "_".join(parts)


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [
        convert_camel_case_to_underscrore_str(column) for column in df.columns
    ]
    df.columns = [rearrange_string(column) for column in df.columns]
    df = df.rename(columns={"id": "id_short"})
    return df


x = TypeVar("x")


def instantiate_type(df: pd.DataFrame, type: Type[x]) -> List[x]:
    df = rename_columns(df)
    items = []
    for index, row in df.iterrows():
        items.append(type(**row.to_dict()))
    return items


class FlexisTransformModel(AbstractTransformModel):
    _orignal_model: FlexisDataFrames = PrivateAttr(default=None)
    _target_model: FlexisDataModel = PrivateAttr(default=None)

    def __init__(self, **data):
        super().__init__(**data)
        # this could also be done with default_factory
        self._orignal_model = None
        self._target_model = None

    @classmethod
    def from_origin(cls, original_model: FlexisDataFrames):
        resources = instantiate_type(original_model.resources, flexisv1.Resource)
        positions = instantiate_type(
            original_model.resource_positions, flexisv1.Position
        )
        resource_types = instantiate_type(
            original_model.resource_types, flexisv1.ResourceType
        )
        resource_variants = instantiate_type(
            original_model.resource_variant, flexisv1.ResourceVariant
        )
        resource_availibility = instantiate_type(
            original_model.resource_availibility, flexisv1.ResourceAvailibility
        )
        resource_tasks = instantiate_type(
            original_model.resource_task, flexisv1.ResourceTask
        )
        tasks = instantiate_type(original_model.tasks, flexisv1.Task)
        work_plans = instantiate_type(original_model.work_plan, flexisv1.WorkPlan)
        work_plan_tasks = instantiate_type(
            original_model.work_plan_task, flexisv1.WorkPlanTask
        )
        setup_times = instantiate_type(original_model.setup_times, flexisv1.SetupTime)
        process_times = instantiate_type(
            original_model.process_times, flexisv1.ProcessTime
        )
        transport_times = instantiate_type(
            original_model.transport_times, flexisv1.TransportTime
        )
        jobs = instantiate_type(
            original_model.job_shop_scheduling_job, flexisv1.Job
        )
        job_tasks = instantiate_type(
            original_model.job_shop_scheduling_job_task, flexisv1.JobTask
        )
        scheduled_job_tasks = instantiate_type(
            original_model.job_shop_scheduling_scheduled_task,
            flexisv1.ScheduledJobTask,
        )
        scenarios = instantiate_type(original_model.scenarios, flexisv1.Scenario)

        flat_model = FlexisDataModel()
        flat_model.load_models(
            resources
            + positions
            + resource_types
            + resource_availibility
            + resource_tasks
            + tasks
            + work_plans
            + work_plan_tasks
            + setup_times
            + process_times
            + transport_times
            + jobs
            + job_tasks
            + scheduled_job_tasks
            + resource_variants
            + scenarios
        )
        instance = cls()
        instance.set_origin(original_model)
        instance.set_target(flat_model)
        return instance

    def to_target(self) -> REFERABLE_MODEL:
        return self._target_model
