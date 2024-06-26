import os
import json
import olca_ipc as ipc
import olca_schema as o
import uuid
import requests
from typing import Callable
from openpyxl import Workbook



# Define the base URL for the server
BASE_URL = "http://127.0.0.1:8000"

# Define the paths for each AAS type
PATHS = {
    "Product": "/Product/",
    "Process": "/Process/",
    "Procedure": "/Procedure/"
}

# Directory where JSON files are stored
JSON_DIRECTORY = "Stellmotor_Skript"  # Adjust this if your JSON files are in a different directory

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

# Initialize the IPC client for openLCA
client = ipc.Client(8083)

# Load the product information from the Server file
product_id = "product_001"
motor_data = get_json(BASE_URL + PATHS["Product"] + f"{product_id}")
print(f"Retrieved product data for {product_id}")

# Extract the overall product description from the JSON
overall_motor_name = motor_data['id_short']

# Define flow properties (Assuming these properties exist in your openLCA database)
mass = client.find(o.FlowProperty, name="Mass")
energy = client.find(o.FlowProperty, name="Energy")
items = client.find(o.FlowProperty, name="Number of items")

# Define units 
group_ref_mass = client.find(o.UnitGroup, "Units of mass")
group = client.get(o.UnitGroup, group_ref_mass.id)
unit_kg = [u for u in group.units if u.name == "kg"]

group_ref_items = client.find(o.UnitGroup, "Units of items")
group = client.get(o.UnitGroup, group_ref_items.id)
unit_items = [u for u in group.units if u.name == "Item(s)"]

group_ref_energy = client.find(o.UnitGroup, "Units of energy")
group = client.get(o.UnitGroup, group_ref_energy.id)
unit_kWh = [u for u in group.units if u.name == "kWh"]

# Create dictionaries to keep track of flows and processes
flow_dict = {}
process_dict = {}

# Function to create a new process
def new_process(name):
    process = o.Process()
    process.name = name
    return process

# Create Flow for the overall motor using the extracted name
flow_name = overall_motor_name  # Use the overall description
flow = o.new_flow(flow_name, o.FlowType.PRODUCT_FLOW, items)
flow.id = str(uuid.uuid4())  # Generate a unique ID for the flow
flow.category = "Stellmotor_Skript"
flow.flow_type = o.FlowType.PRODUCT_FLOW
client.put(flow)
flow_dict[flow_name] = flow.id  # Store the flow ID by name
print(f"Created flow: {flow.name} with ID: {flow.id}")

# Create Process for the overall motor using the extracted name
motor_process_name = overall_motor_name  # Use the overall description
motor_process = new_process(motor_process_name)
motor_process.id = str(uuid.uuid4())  # Generate a unique ID for the process
motor_process.category = "Stellmotor_Skript"
client.put(motor_process)
process_dict[motor_process_name] = motor_process.id  # Store the process ID by name
print(f"Created process: {motor_process.name} with ID: {motor_process.id}")

# Set the output for the over motor process
process_name = motor_process_name
flow_id = flow_dict[process_name]
process_id = process_dict[process_name]
flow = client.get(o.Flow, flow_id)
process = client.get(o.Process, process_id)
output = o.new_output(process, flow, amount=1, unit=items)
output.is_quantitative_reference = True
print(f"Set output for process: {process.name} to flow: {flow.name}")

# Update the process with the new output
client.put(process)

print(f"Basic Setup for following Product Complete: {process.name}")

