import os
import json
import olca_ipc as ipc
import olca_schema as o
import uuid
import requests
import Method_Toolbox
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

# Initialize the IPC client for openLCA
client = ipc.Client(8083)

# Load the product information from the Server file
product_id = "product_001" # Specify the Product ID Here
motor_data = Method_Toolbox.get_json(BASE_URL + PATHS["Product"] + f"{product_id}")
print(f"Retrieved product data for {product_id}")

# Extract the overall product description from the JSON
overall_motor_name = motor_data['id_short']

# Define flow properties 
items = client.find(o.FlowProperty, name="Number of items")

# Define units 
group_ref_items = client.find(o.UnitGroup, "Units of items")
group = client.get(o.UnitGroup, group_ref_items.id)
unit_items = [u for u in group.units if u.name == "Item(s)"]

# Create dictionaries to keep track of flows and processes
flow_dict = {}
process_dict = {}

# Function to create a new process
def new_process(name):
    process = o.Process()
    process.name = name
    return process

# Check if the flow already exists
flow_name = overall_motor_name
existing_flows = client.find(o.Flow, name=flow_name)
if existing_flows:
    flow = existing_flows
    flow_dict[flow_name] = flow.id
    print(f"Flow already exists: {flow.name} with ID: {flow.id}")
else:
    # Create Flow for the overall motor using the extracted name
    print(f"Creating new flow: {flow_name}")
    flow = o.new_flow(flow_name, o.FlowType.PRODUCT_FLOW, items)
    flow.id = str(uuid.uuid4())  # Generate a unique ID for the flow
    flow.category = "Stellmotor_Skript"
    flow.flow_type = o.FlowType.PRODUCT_FLOW
    client.put(flow)
    flow_dict[flow_name] = flow.id  # Store the flow ID by name
    print(f"Created flow: {flow.name} with ID: {flow.id}")

# Check if the process already exists
motor_process_name = overall_motor_name
existing_processes = client.find(o.Process, name=motor_process_name)
if existing_processes:
    motor_process = existing_processes
    process_dict[motor_process_name] = motor_process.id
    print(f"Process already exists: {motor_process.name} with ID: {motor_process.id}")
else:
    # Create Process for the overall motor using the extracted name
    print(f"Creating new process: {motor_process_name}")
    motor_process = new_process(motor_process_name)
    motor_process.id = str(uuid.uuid4())  # Generate a unique ID for the process
    motor_process.category = "Stellmotor_Skript"
    client.put(motor_process)
    process_dict[motor_process_name] = motor_process.id  # Store the process ID by name
    print(f"Created process: {motor_process.name} with ID: {motor_process.id}")

# Set the output for the motor process if not already set
print(f"Setting output for process: {motor_process_name}")
flow_id = flow_dict[flow_name]
process_id = process_dict[motor_process_name]
flow = client.get(o.Flow, flow_id)
process = client.get(o.Process, process_id)

# Check if the output is already set
output_exists = any(exc.flow.id == flow.id and not exc.is_input for exc in process.exchanges)
if output_exists:
    print(f"Output for process: {process.name} to flow: {flow.name} already exists")
else:
    print(f"Creating output for process: {process.name} to flow: {flow.name}")
    output = o.Exchange()
    output.flow = flow
    output.amount = 1
    output.unit = unit_items[0]
    output.is_output = True
    output.is_quantitative_reference = True
    process.exchanges.append(output)
    client.put(process)
    print(f"Set output for process: {process.name} to flow: {flow.name}")

print(f"Basic Setup for the following Product Complete: {process.name}")
