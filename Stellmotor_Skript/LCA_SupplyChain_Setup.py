import os
import json
import pandas as pd
import olca_ipc as ipc
import olca_schema as o
import uuid
from typing import Callable
from openpyxl import Workbook

# Paths to the data files
product_json_path =os.path.join('Stellmotor_Skript', 'Input_Files', 'AAS_motor_example.json')
procedures_json_path = os.path.join('Stellmotor_Skript', 'Output', 'attached_procedures.json')
bom_excel_path = r'C:\Users\juliu\OneDrive\Dokumente\GitHub\MA_DPP\Stellmotor_Skript\Input_Files\24-06-20_Supplementary Excel.xlsx' # Change path to the Supplementary Excel

# Initialize the IPC client for openLCA
client = ipc.Client(8083)

# Load the product information from the JSON file
with open(product_json_path) as f:
    motor_data = json.load(f)

with open(procedures_json_path) as f:
    procedure_data = json.load(f)

# Extract the overall product description from the JSON
overall_motor_name = motor_data['description']

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

# Create mappings from the BOM sheet
bom_data = pd.read_excel(bom_excel_path)
flow_id_mapping = bom_data.set_index('description')['input_flow_id'].to_dict()
weight_mapping = bom_data.set_index('description')['material_weight_input'].to_dict()
items_per_motor_mapping = bom_data.set_index('description')['quantity'].to_dict()

# Create dictionaries to keep track of flows and processes
flow_dict = {}
process_dict = {}

# Function to create a new process
def new_process(name):
    process = o.Process()
    process.name = name
    return process

# Create new flows for each subproduct in the BOM using the original `new_flow` function
for sub_product in motor_data['bom']['sub_products']:
    flow_name = sub_product['description']
    flow = o.new_flow(flow_name, o.FlowType.PRODUCT_FLOW, items)
    flow.id = str(uuid.uuid4())  # Generate a unique ID for the flow
    flow.category = "Stellmotor_Skript"
    flow.flow_type = o.FlowType.PRODUCT_FLOW
    client.put(flow)
    flow_dict[flow_name] = flow.id  # Store the flow ID by name
    print(f"Created flow: {flow.name} with ID: {flow.id}")

# Create new processes and set their output flows to match the flows
for sub_product in motor_data['bom']['sub_products']:
    process_name = sub_product['description']
    process = new_process(process_name)
    process.id = str(uuid.uuid4())  # Generate a unique ID for the process
    process.category = "Stellmotor_Skript"
    client.put(process)
    process_dict[process_name] = process.id  # Store the process ID by name
    print(f"Created process: {process.name} with ID: {process.id}")

# Set the output flow of the processes to the matching flows
for sub_product in motor_data['bom']['sub_products']:
    process_name = sub_product['description']
    flow_id = flow_dict[process_name]
    process_id = process_dict[process_name]

    # Fetch the flow and process objects using their IDs
    flow = client.get(o.Flow, flow_id)
    process = client.get(o.Process, process_id)

    # Create the output for the process
    output = o.new_output(process, flow, amount=1, unit=items)
    print(f"Set output for process: {process.name} to flow: {flow.name}")

    # Update the process with the new output
    client.put(process)

# Set the input flow of the processes from the supplementary excel
for sub_product in motor_data['bom']['sub_products']:
    process_name = sub_product['description']
    
    # Retrieve the corresponding flow_id and weight from the mappings
    flow_id = flow_id_mapping.get(process_name)
    weight = weight_mapping.get(process_name)

    if flow_id and weight:
        # Fetch the flow and process objects using their IDs
        flow = client.get(o.Flow, flow_id)
        process_id = process_dict.get(process_name)  # Get the correct process ID for the current sub-product
        process = client.get(o.Process, process_id)

        # Create the input for the process
        input_flow = o.new_input(process, flow, amount=weight, unit = mass)
        input_flow.unit = unit_kg[0]
        print(f"Set input for process: {process.name} to flow: {flow.name} with weight: {weight}")

        # Update the process with the new input
        client.put(process)
    else:
        print(f"Flow ID or weight not found for process: {process_name}")

print("All processes have been updated with their respective input flows.")
print("Supply Chain Flows and Processes Set Up")

