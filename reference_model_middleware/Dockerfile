ARG APP_VERSION=0.2.1

FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies using Poetry
RUN pip install aas2openapi prodsys aiohttp
COPY ./sdm /app/sdm
COPY ./reference_model_middleware/ /app

EXPOSE 8000

CMD ["uvicorn", "aas_middleware_docker_script:middleware.app", "--host", "0.0.0.0", "--port", "8000"]