import os
import json
import olca_ipc as ipc
import olca_schema as o
import uuid
import requests
import pandas as pd
import Method_Toolbox
from typing import Callable
from openpyxl import Workbook

# Define the base URL for the server
BASE_URL = "http://127.0.0.1:8000" # Change if server URL is differnt

# Define the paths for each AAS type
PATHS = {
    "Product": "/Product/",
    "Process": "/Process/",
    "Procedure": "/Procedure/",
    "Passport": "/Passport/"
}

# Function to get JSON data from the server
def get_json(url):
    response = requests.get(url, allow_redirects=True)  # Allowing redirects
    if response.status_code != 200:
        print(f"Error {response.status_code} for URL: {url}")
        print(f"Response headers: {response.headers}")  # Print response headers
        print(f"Response content: {response.text}")  # Print response content
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
    return response.json()

# Load the product information from the Server file and procedure information from the file
# Retrieve all attached procedures for a given product
def retrieve_procedures_exp(product_id):
    procedure_responses = []
    # Load the product AAS to find the main process
    try:
        product_data = get_json(BASE_URL + PATHS["Product"] + f"{product_id}")
        print(f"Retrieving product data for {product_id}...")
        main_process_id = product_data.get("process_reference", {}).get("process_id")
        if not main_process_id:
            print(f"Main process not found for product {product_id}")
            return procedure_responses
        print(f"Main process ID found: {main_process_id}, searching pocedures...")
    except Exception as e:
        print(f"Failed to get product data for {product_id}: {e}")
        return procedure_responses

    # Load the main process to find attached processes
    try:
        main_process_data = get_json(BASE_URL + PATHS["Process"] + f"{main_process_id}")
        attached_process_ids = main_process_data.get("process_model", {}).get("sequence", [])
    except Exception as e:
        print(f"Failed to get main process data for {main_process_id}: {e}")
        return procedure_responses

    # Retrieve procedure data for each attached process using process attributes
    for process_id in attached_process_ids:
        try:
            # Fetch the process data to get the process attributes
            process_data = get_json(BASE_URL + PATHS["Process"] + f"{process_id}")
            process_attributes = process_data.get("process_attributes", {}).get("id_short")
            if process_attributes: # Change this once the middleware is working to match using "process-attributes" instead
                # Derive the procedure ID from the process ID
                procedure_id = f"procedure_{process_id.split('_', 1)[1]}"
                # Construct the full URL for the procedure
                procedure_url = BASE_URL + PATHS["Procedure"] + f"{procedure_id}"
                # Fetch the procedure data using the derived procedure ID
                procedure_data = get_json(procedure_url)
                procedure_responses.append(procedure_data)
            else:
                print(f"No process attributes found for process {process_id}")
        except Exception as e:
            print(f"Failed to get procedure data for {process_id}: {e}")

    print("Completed retrieval of all attached procedures.")
    return procedure_responses


product_id = "product_001" # Adjust using User Input

motor_data = get_json(BASE_URL + PATHS["Product"] + f"{product_id}")

# Load Procedure data from SDM Model for Power Consumption Calculation
procedure_data = retrieve_procedures_exp(product_id)
print(f"Retrieved procedure data for {product_id}")

print(procedure_data)

