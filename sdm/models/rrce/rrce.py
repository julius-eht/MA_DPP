from typing import Optional, List, Union
from pydantic import BaseModel
from sdm.model_core.data_model import DataModel
from aas2openapi.models.base import Referable


class Performance(Referable):
    cycle_time: Optional[float]

class Resource(Referable):
    production_level: Optional[str]
    resource_type: Optional[str]
    cad_file: Optional[str]
    position: List[float]
    orientation: List[float]

class RrceModel(DataModel):
    def __init__(self, *models: Union[List[BaseModel], BaseModel]):
        super().__init__(*models)
        self.models = {}

    @property
    def performances(self) -> List[Performance]:
        return self.get_models_of_type(Performance)

    @property
    def resources(self) -> List[Resource]:
        return self.get_models_of_type(Resource)
