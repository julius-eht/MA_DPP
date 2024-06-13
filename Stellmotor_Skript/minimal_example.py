import typing
import aas2openapi
from aas2openapi.middleware import Middleware
from aas2openapi import models
from enum import Enum

import models.product
print("Attributes in models.product:", dir(models.product))

# Create a product instance

example_product = Product(
    id="TTN01_example_instances",
    description="Steering axle for a car of type TTN01",
    id_short="TTN01_example_instances",
    bom=BOM(
        id="TTN01_bom",
        id_short="TTN01_bom",
        description="Bill of materials for a steering axle TTN01",
        semantic_id="http://purl.obolibrary.org/obo/PROCO_0000284",
        sub_product_count=1,
        subProduct=[
            SubProduct(
                id="sensordeckel_sub_product",
                id_short="sensordeckel_sub_product",
                product_type="sensordeckel",
                product_id="sensordeckel_1234",
                status="unassembled",
                quantity=1,
                product_use_type="assembled",
            ),
            SubProduct(
                id="sensordeckel_sub_product",
                id_short="sensordeckel_sub_product",
                product_type="sensordeckel",
                product_id="sensordeckel_1234",
                status="unassembled",
                quantity=1,
                product_use_type="assembled",
            ),
        ]
    ),
    process_reference=ProcessReference(
        id="TTN01_process_reference",
        id_short="TTN01_process_reference",
        description="Process for assembling a steering axle",
        semantic_id="https://ontobee.org/ontology/OBI?iri=http://purl.obolibrary.org/obo/OBI_0000011",
        process_id="TTN01_Herstellungsprozess",
    ),
    construction_data=ConstructionData(
        id="steering_axle_construction_data",
        cad_file="https://grabcad.com/library/steering-axle-3",
    ),
    product_information=ProductInformation(
        id="TTN01_General_Information",
        description="General information of TTN01",
        id_short="TTN01_General_Information",
        product_type="TTN01",
        manufacturer="Bosch"
    )
)


obj_store = aas2openapi.convert_pydantic_model_to_aas(example_product)

import basyx.aas.adapter.json.json_serialization

with open("examples/simple_aas_and_submodels.json", "w", encoding="utf-8") as json_file:
    basyx.aas.adapter.json.write_aas_json_file(json_file, obj_store)

# Reverse transformation

data_model = aas2openapi.convert_object_store_to_pydantic_models(obj_store)

# Create the middleware and load the models
middleware = Middleware()

middleware.load_pydantic_models([Product])
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
