import requests
import json
import os
from datetime import datetime

# Define the base URL for the server
BASE_URL = "http://127.0.0.1:8000"

# Define the paths for each AAS type
PATHS = {
    "Product": "/Product/",
    "Process": "/Process/",
    "Procedure": "/Procedure/",
    "Passport": "/Passport/",
}

# Headers to match manual upload (Postman)
headers = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "User-Agent": "PostmanRuntime/7.39.0"  # This mirrors the User-Agent from the manual upload
}

# Function to get JSON data from the server
def get_json(url):
    print(f"Attempting to GET data from URL: {url}")  # Debug line to print the exact URL being requested
    response = requests.get(url, allow_redirects=True)  # Allowing redirects
    print(f"Response status code: {response.status_code}")  # Debug line to show status code
    if response.status_code != 200:
        print(f"Error {response.status_code} for URL: {url}")
        print(f"Response headers: {response.headers}")  # Print response headers
        print(f"Response content: {response.text}")  # Print response content
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
    return response.json()

# Retrieve all attached procedures for a given product
def retrieve_attached_procedures(product_id):
    procedure_responses = []
    # Load the product AAS to find the main process
    try:
        product_data = get_json(BASE_URL + PATHS["Product"] + f"{product_id}")
        print(f"Retrieved product data for {product_id}")
        main_process_id = product_data.get("process_reference", {}).get("process_id")
        if not main_process_id:
            print(f"Main process not found for product {product_id}")
            return procedure_responses
        print(f"Main process ID found: {main_process_id}")
    except Exception as e:
        print(f"Failed to get product data for {product_id}: {e}")
        return procedure_responses

    # Load the main process to find attached processes
    try:
        main_process_data = get_json(BASE_URL + PATHS["Process"] + f"{main_process_id}")
        print(f"Retrieved main process data for {main_process_id}")
        attached_process_ids = main_process_data.get("process_model", {}).get("sequence", [])
        print(f"Attached process IDs found: {attached_process_ids}")
    except Exception as e:
        print(f"Failed to get main process data for {main_process_id}: {e}")
        return procedure_responses

    # Retrieve procedure data for each attached process using process attributes
    for process_id in attached_process_ids:
        try:
            print(f"Processing attached process ID: {process_id}")
            # Fetch the process data to get the process attributes
            process_data = get_json(BASE_URL + PATHS["Process"] + f"{process_id}")
            process_attributes = process_data.get("process_attributes", {}).get("id_short")
            if process_attributes:
                # Derive the procedure ID from the process ID
                procedure_id = f"procedure_{process_id.split('_', 1)[1]}"
                print(f"Derived procedure ID: {procedure_id}")
                # Construct the full URL for the procedure
                procedure_url = BASE_URL + PATHS["Procedure"] + f"{procedure_id}"
                print(f"Attempting to GET procedure data from URL: {procedure_url}")  # Debug line to print procedure URL
                # Fetch the procedure data using the derived procedure ID
                procedure_data = get_json(procedure_url)
                print(f"Retrieved procedure data for {procedure_id}")
                procedure_responses.append(procedure_data)
            else:
                print(f"No process attributes found for process {process_id}")
        except Exception as e:
            print(f"Failed to get procedure data for {process_id}: {e}")

    print("Completed retrieval of all attached procedures.")
    return procedure_responses

def retrieve_total_pcf(passport_id: str) -> float:
    total_pcf = 0.0

    # Load the product AAS to find the BOM
    try:
        product_data = get_json(BASE_URL + PATHS["Passport"] + f"{passport_id}")
        print(f"Retrieved product data for {passport_id}")
        bom = product_data.get("bom", {})
        if not bom:
            print(f"BOM not found for product {passport_id}")
            return total_pcf
        sub_products = bom.get("sub_products", [])
        print(f"Sub-products found: {sub_products}")
    except Exception as e:
        print(f"Failed to get product data for {passport_id}: {e}")
        return total_pcf

    # Retrieve PCF data for each sub-product
    for sub_product in sub_products:
        try:
            sub_passport_id = sub_product.get("passport_id")
            if not sub_passport_id:
                print(f"No passport ID found for sub-product: {sub_product}")
                continue

            print(f"Processing passport ID: {sub_passport_id}")
            # Fetch the sub-product passport data to get the carbon footprint
            passport_data = get_json(BASE_URL + PATHS["Passport"] + f"{sub_passport_id}")
            carbon_footprint = passport_data.get("carbon_footprint", {})

            if carbon_footprint:
                # Aggregate PCF values
                product_footprints = carbon_footprint.get("product_footprint", [])
                for pcf in product_footprints:
                    total_pcf += pcf.get("PCFCO2eq", 0.0)
            else:
                print(f"No carbon footprint data found for passport ID: {sub_passport_id}")
        except Exception as e:
            print(f"Failed to get passport data for passport ID {sub_passport_id}: {e}")

    print("Completed retrieval and aggregation of all PCF data.")
    return total_pcf

def retrieve_total_tcf(passport_id: str) -> float:
    total_tcf = 0.0

    # Load the product AAS to find the BOM
    try:
        product_data = get_json(BASE_URL + PATHS["Product"] + f"{passport_id}")
        print(f"Retrieved product data for {passport_id}")
        bom = product_data.get("bom", {})
        if not bom:
            print(f"BOM not found for product {passport_id}")
            return total_tcf
        sub_products = bom.get("sub_products", [])
        print(f"Sub-products found: {sub_products}")
    except Exception as e:
        print(f"Failed to get product data for {passport_id}: {e}")
        return total_tcf

    # Retrieve TCF data for each sub-product
    for sub_product in sub_products:
        try:
            sub_passport_id = sub_product.get("passport_id")
            if not passport_id:
                print(f"No passport ID found for sub-product: {sub_product}")
                continue

            print(f"Processing passport ID: {sub_passport_id}")
            # Fetch the sub-product passport data to get the carbon footprint
            passport_data = get_json(BASE_URL + PATHS["Passport"] + f"{sub_passport_id}")
            carbon_footprint = passport_data.get("carbon_footprint", {})

            if carbon_footprint:
                # Aggregate TCF values
                transport_footprints = carbon_footprint.get("transport_footprint", [])
                for tcf in transport_footprints:
                    total_tcf += tcf.get("TCFCO2eq", 0.0)
            else:
                print(f"No carbon footprint data found for passport ID: {sub_passport_id}")
        except Exception as e:
            print(f"Failed to get passport data for passport ID {sub_passport_id}: {e}")

    print("Completed retrieval and aggregation of all TCF data.")
    return total_tcf