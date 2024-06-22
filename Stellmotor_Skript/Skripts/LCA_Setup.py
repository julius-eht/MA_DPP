import json
import pandas as pd
import olca_ipc as ipc
import olca_schema as o
import uuid
from typing import Callable
from openpyxl import Workbook

# Paths to the data files
product_json_path = r'C:\Users\juliu\OneDrive\Desktop\Arbeitsdatein MA Skript\AAS_motor_example.json'
procedures_json_path = r'C:\Users\juliu\OneDrive\Desktop\Arbeitsdatein MA Skript\AAS_list_procedure.json'
bom_excel_path = r'C:\Users\juliu\OneDrive\Desktop\Arbeitsdatein MA Skript\24-06-20_Supplementary Excel.xlsx'

# Initialize the IPC client for openLCA
client = ipc.Client(8080)

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

# Initialize total power consumption
total_power_consumption = 0.0

# Assume power_input_data is a list of procedures each containing a 'power_consumption' field, calculate value for later insertion into process
for procedure in procedure_data:
    # Ensure 'procedure_emission' exists and has 'power_consumption'
    if 'procedure_emission' in procedure and 'power_consumption' in procedure['procedure_emission']:
        power_consumption = procedure['procedure_emission']['power_consumption']
        total_power_consumption += power_consumption
    else:
        print(f"No power consumption data available for procedure: {procedure['id_short']}")

print(f"Total power consumption from all procedures: {total_power_consumption} kWh")

# Fetch the overall motor process object using its ID
overall_process = client.get(o.Process, process_dict[overall_motor_name])

# Initialize the list of input exchanges for the overall motor process
input_exchanges = []

# Set component flows as input flows for the overall motor
for sub_product in motor_data['bom']['sub_products']:
    sub_product_name = sub_product['description']
    flow_id = flow_dict.get(sub_product_name)
    items_per_motor = items_per_motor_mapping.get(sub_product_name, 1)  # Default to 1 if not found

    if flow_id and items_per_motor:
        # Fetch the flow object using its ID
        sub_product_flow = client.get(o.Flow, flow_id)
        
        # Create the input flow for the overall motor process
        input_exchange = o.Exchange()
        input_exchange.flow = sub_product_flow
        input_exchange.amount = items_per_motor
        input_exchange.unit = unit_items[0]
        input_exchange.is_input = True  # Indicate that this is an input exchange

        # Append the input exchange to the list of input exchanges
        input_exchanges.append(input_exchange)

        print(f"Set input for overall motor process: {overall_process.name} to flow: {sub_product_flow.name} with quantity: {items_per_motor}")

# Add Power Consumption Flow
power_flow = client.get(o.Flow, uid="4f19a2f2-7b3b-11dd-ad8b-0800200c9a66")

if power_flow:
    # Create the input flow for the overall motor process with only the electrical power from before
    power_exchange = o.Exchange()
    power_exchange.flow = power_flow
    power_exchange.amount = total_power_consumption
    power_exchange.unit = unit_kWh[0]
    power_exchange.is_input = True  # Indicate that this is an input exchange

    # Append the input exchange to the list of input exchanges
    input_exchanges.append(power_exchange)

    print(f"Set input for overall motor process: {overall_process.name} to flow: {power_flow.name} with quantity: {total_power_consumption} kWh")

# Retrieve existing exchanges and add new input exchanges
if overall_process.exchanges:
    # Filter out existing inputs (if any) to avoid duplication
    existing_exchanges = [ex for ex in overall_process.exchanges if not ex.is_input]
else:
    existing_exchanges = []

# Combine existing exchanges with the new input exchanges
combined_exchanges = existing_exchanges + input_exchanges

# Assign the combined list of exchanges back to the overall motor process
overall_process.exchanges = combined_exchanges

# Update the overall motor process with the combined exchanges
client.put(overall_process)
print(f"All component and energy flows have been set as input flows for the overall motor process: {overall_process.name}")

# Build Product System
overall_process_ref = client.find(o.Process, motor_process_name)
config = o.LinkingConfig(
    prefer_unit_processes=False,
    provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
)
overall_product_system = client.create_product_system(overall_process_ref,config)

# Conduct the acutal LCA
# Select the impact method
impact_method = "83812f2a-8272-3244-91a5-20ca745f0902"

# create a calculation setup
setup = o.CalculationSetup(
    target=o.Ref(
        ref_type=o.RefType.ProductSystem,
        id= overall_product_system.id,
    ),
    impact_method=o.Ref(id=impact_method),
    nw_set= None,
    amount= 10.0
)

# run a calculation
result: ipc.Result = client.calculate(setup)
result.wait_until_ready()

#Save the results
# Check if there was an error in the result
# Check for errors
if result.error:
    print(f"Error during calculation: {result.error}")
else:
    # Extract Total Impacts
    total_impacts_data = []
    for impact_value in result.get_total_impacts():
        total_impacts_data.append({
            "Impact Category": impact_value.impact_category.name,
            "Amount": impact_value.amount,
        })
    df_total_impacts = pd.DataFrame(total_impacts_data)
    
    # Extract Tech Flows
    tech_flows_data = []
    for tech_flow in result.get_tech_flows():
        tech_flows_data.append({
            "Flow Name": tech_flow.flow.name,
        })
    df_tech_flows = pd.DataFrame(tech_flows_data)
    
    # Extract Environmental Flows
    envi_flows_data = []
    for envi_flow in result.get_envi_flows():
        envi_flows_data.append({
            "Flow Name": envi_flow.flow.name,
        })
    df_envi_flows = pd.DataFrame(envi_flows_data)

    # Define the path to save the Excel file
    excel_file_path = r'C:\Users\juliu\OneDrive\Desktop\Arbeitsdatein MA Skript'

    print(df_total_impacts,df_tech_flows,df_envi_flows)

