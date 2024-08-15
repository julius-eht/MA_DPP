import abc

from sdm.adapters.simplan_adapters.reference_model_wrapper import ReferenceModelWrapper
from sdm.models.sdm_reference_model.reference_model import Resource
from sdm.models.simplan.model import AbstractNodeItem


class ItemFactory(abc.ABC):
    def __init__(self, ref_model: ReferenceModelWrapper):
        self.ref_model = ref_model

    @abc.abstractmethod
    def create(self, resource: Resource, common: dict) -> AbstractNodeItem:
        ...
