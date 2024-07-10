import typing
import aas2openapi
from aas2openapi.middleware import Middleware

from models.product import (
        Product,
    )

from models.processes import (
    Process,
)

from models.procedure import (
    Procedure
)

from models.passport import (
    Passport
)

# Create the middleware and load the models
middleware = Middleware()

middleware.load_pydantic_models([Product, Process, Procedure, Passport])
middleware.generate_rest_api()
middleware.generate_model_registry_api()

app = middleware.app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
