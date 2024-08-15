from typing import Set

from sdm.adapters.simplan_adapters.factory.node import NodeFactory
from sdm.adapters.simplan_adapters.reference_model_wrapper import ReferenceModelWrapper
from sdm.models.sdm_reference_model.reference_model import ReferenceModel
from sdm.models.simplan.model import AbstractNodeItem, SimJSON

SimplanModel = SimJSON

"""
TODO: Deal with optional values, which are required in SimJSON
TODO: Deal with different timemodel distributions
"""


def transform_reference_model(reference_model: ReferenceModel) -> SimplanModel:
    """
    Transforms a production system represented in the sdm reference model to a simplan model.

    Args:
        reference_model (ReferenceModel): The reference model to transform.

    Returns:
        SimplanModel: The transformed production system model.
    """

    return SimplanAdapter(reference_model).as_sim_json()


class SimplanAdapter:
    def __init__(self, reference_model: ReferenceModel):
        self.reference_model = ReferenceModelWrapper(reference_model)

    def as_sim_json(self) -> SimplanModel:
        return self.__create_sim_json()

    def __create_sim_json(self) -> SimplanModel:
        return SimJSON.parse_obj(
            {
                "simulationJob": {
                    "id": 11,
                    "name": "Project_Model_ARENA2036_basicUsecase",
                    "settings": {
                        "simulationStartDate": "2023-02-13T00:00:00Z",
                        "simulationEndDate": "2023-02-14T00:00:00Z",
                        "initialStatsOffsetInHours": 0,
                        "simulationApiVersion": "v360",
                        "userLanguage": "de",
                        "randomNumbersVariant": 1,
                    },
                    "alternatives": [
                        {
                            "id": 14,
                            "name": "Model_ARENA2036_basicUsecase",
                            "model": {
                                "linkDataArray": [],
                                "nodeDataArray": self.__create_nodes(),
                            },
                        }
                    ],
                }
            }
        )

    def __create_nodes(self) -> Set[AbstractNodeItem]:
        nodes = set()
        factory = NodeFactory(
            ref_model=self.reference_model,
        )
        for resource in self.reference_model.resources:
            if resource.resource_information.production_level == "Station":
                node = factory.create(resource)
                if node is not None:
                    nodes.add(node)
        return nodes
