from sdm.adapters.simplan_adapters.factory.item import ItemFactory
from sdm.adapters.simplan_adapters.reference_model_wrapper import ReferenceModelWrapper
from sdm.models.sdm_reference_model.reference_model import Resource
from sdm.models.simplan.model import AbstractNodeItem


class SinkFactory(ItemFactory):
    def create(self, resource: Resource, common: dict):
        return AbstractNodeItem(**common, **{"class": "drain", "parameters": []})
