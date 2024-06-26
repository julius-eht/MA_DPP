import typing
import aas2openapi
from aas2openapi.middleware import Middleware

from models.product import (
        ProcessReference,
        Product,
        ProductInformation,
        ProductUseType,
        SubProduct,
        BOM,
        TrackingData,
        ConstructionData
    )


from models.processes import (
    Process,
    ProcessInformation,
    AttributePredicate,
    ProcessAttributes,
    ProcessModelType,
    ProcessModel
)

from models.procedure import (
    ProcedureTypeEnum,
    ActivityTypeEnum,
    Event,
    ExecutionModel,
    TimeModel,
    ProcedureInformation,
    GreenHouseGasEmission,
    ProcedureEmission,
    Procedure
)

# Create the middleware and load the models
middleware = Middleware()

middleware.load_pydantic_models([Product, Process, Procedure])
# middleware.load_pydantic_model_instances([example_product, example_process])
# middleware.load_aas_objectstore(obj_store)
# middleware.load_json_models(file_path="examples/example_json_model.json")
middleware.generate_rest_api()
# middleware.generate_graphql_api()
middleware.generate_model_registry_api()

app = middleware.app
#run with: uvicorn examples.minimal_example:app --reload
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
