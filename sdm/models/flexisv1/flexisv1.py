from typing import Any, Optional, Union, List
import uuid

import pandas as pd
from pydantic import root_validator, validator
from aas2openapi.models.base import Referable
import datetime

from sdm.model_core.data_model import DataModel



def date_time_string_to_duration(value: str) -> float:
    """
    Convert a string in the format %H:%M:%S.%f to a float in minutes.

    Args:
        value (str): String in the format %H:%M:%S.%f, e.g. 00:00:00.000

    Returns:
        float: Duration in minutes
    """
    if isinstance(value, float):
        return value
    return (datetime.datetime.strptime(value, "%H:%M:%S.%f") - datetime.datetime.strptime("00:00:00", "%H:%M:%S")).total_seconds()


def date_time_string_to_datetime(value: str | datetime.datetime) -> str:
    """
    Convert a string in the format %H:%M:%S.%f to a datetime object.

    Args:
        value (str): String in the format %H:%M:%S.%f, e.g. 2023-06-23 00:00:00.000

    Returns:
        datetime: Datetime object
    """
    if isinstance(value, str):
        if "T" in value:
            return datetime.datetime.fromisoformat(value).isoformat()
        else:
            return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f").isoformat()
    if not isinstance(value, datetime.datetime):
        raise TypeError("value must be of type str or datetime.datetime")
    return value.isoformat()

class SetupTime(Referable):
    duration: float
    resource_id: str
    task_from_id: str
    task_to_id: str

    @validator("duration", pre=True)
    def duration_to_timedelta(cls, v):
        return date_time_string_to_duration(v)

class ProcessTime(Referable):
    duration: float
    resource_id: str
    task_id: str

    @validator("duration", pre=True)
    def duration_to_timedelta(cls, v):
        return date_time_string_to_duration(v)

class TransportTime(Referable):
    duration: float

    @validator("duration", pre=True)
    def duration_to_timedelta(cls, v: pd.Timestamp):
        return date_time_string_to_duration(v)

class Task(Referable):
    name: str


class ResourceTask(Referable):
    resource_id: str
    task_id: str


class Resource(Referable):
    locale: str
    name: str
    type_id: str
    capacity_max: Optional[Union[str, int]]
    parent_id: Optional[str]
    position_id: Optional[str]


class ResourceType(Referable):
    name: str

class Position(Referable):
    x_coordinate: float
    y_coordinate: float
    angle: float


class ResourceAvailibility(Referable):
    resource_id: str
    availibility: float
    mttf: float
    mttr: float

    @validator("mttf", pre=True)
    def duration_to_timedelta(cls, v: pd.Timestamp):
        return date_time_string_to_duration(v)

    @validator("mttr", pre=True)
    def duration_to_timedelta2(cls, v: pd.Timestamp):
        return date_time_string_to_duration(v)


class ResourceVariant(Referable):
    resource_id: str
    cad_file_name: str


class WorkPlan(Referable):
    name: str


class WorkPlanTask(Referable):
    sequence: int
    task_id: str
    work_plan_id: str

class Job(Referable):
    work_plan_id: str
    name: str	
    release_date: str
    due_date: str
    target_date: str

    @validator("release_date", pre=True)
    def duration_to_timedelta(cls, v):
        return date_time_string_to_datetime(v)
    
    @validator("due_date", pre=True)
    def duration_to_timedelta2(cls, v):
        return date_time_string_to_datetime(v)
    
    @validator("target_date", pre=True)
    def duration_to_timedelta3(cls, v):
        return date_time_string_to_datetime(v)

class JobTask(Referable):
    job_id: str
    name: str
    sequence: int
    task_id: str


class ScheduledJobTask(Referable):
    job_task_id: str
    process_begin_date: str
    process_end_date: str
    resource_id: str
    arrival_date: str
    departure_date: str
    setup_begin_date: str
    teardown_end_date: str

    @root_validator(pre=True)
    def set_id_short(cls, values):
        id_short = "u" + str(uuid.uuid1()).replace("-", "_")
        values["id_short"] = id_short
        return values

    @validator("process_begin_date", pre=True)
    def duration_to_timedelta(cls, v):
        return date_time_string_to_datetime(v)
    
    @validator("process_end_date", pre=True)
    def duration_to_timedelta2(cls, v):
        return date_time_string_to_datetime(v)
    
    @validator("arrival_date", pre=True)
    def duration_to_timedelta3(cls, v):
        return date_time_string_to_datetime(v)
    
    @validator("departure_date", pre=True)
    def duration_to_timedelta4(cls, v):
        return date_time_string_to_datetime(v)
    
    @validator("setup_begin_date", pre=True)
    def duration_to_timedelta5(cls, v):
        return date_time_string_to_datetime(v)
    
    @validator("teardown_end_date", pre=True)
    def duration_to_timedelta6(cls, v):
        return date_time_string_to_datetime(v)

class Scenario(Referable):
    reconfiguration_type: str	
    resource_id: str
    max_reconfiguration_cost: float	
    max_number_of_machines: int	
    max_number_of_transport_resources: int
    max_number_of_process_modules_per_resource: int


class FlexisDataModel(DataModel):
    @property
    def setup_times(self) -> List[SetupTime]:
        return self.get_models_of_type(self, SetupTime)
    
    @property
    def process_times(self) -> List[ProcessTime]:
        return self.get_models_of_type(self, ProcessTime)
    
    @property
    def transport_times(self) -> List[TransportTime]:
        return self.get_models_of_type(self, TransportTime)
    
    @property
    def tasks(self) -> List[Task]:
        return self.get_models_of_type(self, Task)
    
    @property
    def resource_tasks(self) -> List[ResourceTask]:
        return self.get_models_of_type(self, ResourceTask)
    
    @property
    def resources(self) -> List[Resource]:
        return self.get_models_of_type(self, Resource)
    
    @property
    def resource_availibilities(self) -> List[ResourceAvailibility]:
        return self.get_models_of_type(self, ResourceAvailibility)
    
    @property
    def resource_variants(self) -> List[ResourceVariant]:
        return self.get_models_of_type(self, ResourceVariant)
    
    @property
    def resource_types(self) -> List[ResourceType]:
        return self.get_models_of_type(self, ResourceType)
    
    @property
    def positions(self) -> List[Position]:
        return self.get_models_of_type(self, Position)
    
    @property
    def work_plans(self) -> List[WorkPlan]:
        return self.get_models_of_type(self, WorkPlan)
    
    @property
    def work_plan_tasks(self) -> List[WorkPlanTask]:
        return self.get_models_of_type(self, WorkPlanTask)
    
    @property
    def scenarios(self) -> List[Scenario]:
        return self.get_models_of_type(self, Scenario)
    
    @property
    def jobs(self) -> List[Job]:
        return self.get_models_of_type(self, Job)
    
    @property
    def job_tasks(self) -> List[JobTask]:
        return self.get_models_of_type(self, JobTask)
    
    @property
    def scheduled_job_tasks(self) -> List[ScheduledJobTask]:
        return self.get_models_of_type(self, ScheduledJobTask)


FLEXIS_TYPES_LIST = [WorkPlanTask, ResourceVariant, ResourceAvailibility, ProcessTime, ResourceTask, SetupTime, TransportTime, Job, JobTask, ScheduledJobTask, Task, Resource, ResourceType, Position, WorkPlan, Scenario]
FLEXIS_TYPES = Union[WorkPlanTask, ResourceVariant, ResourceAvailibility, ProcessTime, ResourceTask, SetupTime, TransportTime, Job, JobTask, ScheduledJobTask, Task, Resource, ResourceType, Position, WorkPlan, Scenario]