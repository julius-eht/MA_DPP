from typing import Type, TypeVar

from aas2openapi.models.base import Referable

from sdm.models.sdm_reference_model.reference_model import ReferenceModel

T = TypeVar("T", bound=Referable)


class ReferenceModelWrapper:
    def __init__(self, reference_model: ReferenceModel):
        self.reference_model = reference_model
        self.resources = reference_model.models["resource"]
        self.procedures = reference_model.models["procedure"]
        self.orders = reference_model.models["order"]
        self.products = reference_model.models["product"]
        self.processes = reference_model.models["process"]

    def get_model_of_type(self, id_short: str, type: Type[T]) -> T:
        model = self.reference_model.get_model(id_short)
        if isinstance(model, type):
            return model
        else:
            raise ValueError(f"Model with id_short {id_short} is not of type {type}")
