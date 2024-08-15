from __future__ import annotations
from dotenv import load_dotenv

load_dotenv(".env.docker")

from aas2openapi.middleware import Middleware
from sdm.models.sdm_reference_model import Product, Resource, Procedure, Process, Order, ChangeScenario, Performance
from routers import morpheus_workflows, sdm_workflows

middleware = Middleware()
middleware.load_pydantic_models([Product, Resource, Procedure, Process, Order, ChangeScenario, Performance])
middleware.generate_rest_api()
middleware.app.include_router(sdm_workflows.router)
middleware.app.include_router(morpheus_workflows.router)