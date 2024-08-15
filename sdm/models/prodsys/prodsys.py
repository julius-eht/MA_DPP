from typing import Any, Optional, Union, List
import uuid

import pandas as pd
from pydantic import root_validator, validator
from aas2openapi.models.base import Referable
import datetime

from sdm.model_core.data_model import DataModel

from prodsys import adapters
from prodsys.models import (
    product_data,
    processes_data,
    resource_data,
    time_model_data,
    sink_data,
    source_data,
    state_data,
    scenario_data,
    performance_data
)


class ProdsysModel(DataModel):

    def __init__(self, *models: Union[List[Referable], Referable], adapter: adapters.JsonProductionSystemAdapter):
        super().__init__(*models)
        self.adapter = adapter


    @property
    def time_model_data(self) -> List[time_model_data.TIME_MODEL_DATA]:
        return self.adapter.time_model_data
    
    @property
    def product_data(self) -> List[product_data.ProductData]:
        return self.adapter.product_data
    
    @property
    def processes_data(self) -> List[processes_data.PROCESS_DATA_UNION]:
        return self.adapter.process_data
    
    @property
    def resource_data(self) -> List[resource_data.RESOURCE_DATA_UNION]:
        return self.adapter.resource_data
    
    @property
    def sink_data(self) -> List[sink_data.SinkData]:
        return self.adapter.sink_data
    
    @property
    def source_data(self) -> List[source_data.SourceData]:
        return self.adapter.source_data
    
    @property
    def state_data(self) -> List[state_data.StateData]:
        return self.adapter.state_data
    
    @property
    def scenario_data(self) -> List[scenario_data.ScenarioData]:
        return self.adapter.scenario_data
    
    @property
    def event_data(self) -> List[performance_data.Event]:
        return self.get_models_of_type(self, performance_data.Event)
    @property
    def performance_data(self) -> List[performance_data.Performance]:
        return self.get_models_of_type(self, performance_data.Performance)