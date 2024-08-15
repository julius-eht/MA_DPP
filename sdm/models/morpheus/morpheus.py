from telnetlib import GA
from typing import Any, Optional, Union, List
import uuid

import pandas as pd
from pydantic import root_validator, validator
from aas2openapi.models.base import Referable
import datetime

from sdm.model_core.data_model import DataModel

from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models import (
    ProcessData,
    WorkStation,
    ProductionLine,
    PoleHousing,
    Order, 
    GameRound, 
    Training, 
    Variant, 
    Part, 
    WorkProcess
)
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models.editable_part import EditablePart
from sdm.models.morpheus.morpheus_api_client.morpheus_api_client.models.editable_variant import EditableVariant


class MorpheusModel(DataModel):

    def __init__(self, *models: Union[List[Referable], Referable]):
        super().__init__(*models)
        
    @property
    def process_dates(self) -> List[ProcessData]:
        return self.get_models_of_type(ProcessData)
    
    @property
    def game_rounds(self) -> List[GameRound]:
        return self.get_models_of_type(GameRound)
    
    @property
    def trainings(self) -> List[Training]:
        return self.get_models_of_type(Training)
    
    @property
    def variants(self) -> List[EditableVariant]:
        return self.get_models_of_type(EditableVariant)
    
    @property
    def parts(self) -> List[EditablePart]:
        return self.get_models_of_type(EditablePart)
    
    @property
    def work_processes(self) -> List[WorkProcess]:
        return self.get_models_of_type(WorkProcess)
    
    @property
    def work_stations(self) -> List[WorkStation]:
        return self.get_models_of_type(WorkStation)
    
    @property
    def production_lines(self) -> List[ProductionLine]:
        return self.get_models_of_type(ProductionLine)
    
    @property
    def pole_housings(self) -> List[PoleHousing]:
        return self.get_models_of_type(PoleHousing)
    
    @property
    def orders(self) -> List[Order]:
        return self.get_models_of_type(Order)