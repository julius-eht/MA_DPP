import os
import json
import pandas as pd
import olca_ipc as ipc
import olca_schema as o
from typing import Callable
from openpyxl import Workbook

# Paths to the data files
procedures_json_path = os.path.join('Stellmotor_Skript', 'Output', 'attached_procedures.json')
product_json_path = os.path.join('Stellmotor_Skript', 'Input_Files', 'AAS_motor_example.json')

# Initialize the IPC client for openLCA
client = ipc.Client(8080)

# Load the procedure information from the JSON file
with open(procedures_json_path) as f:
    procedure_data = json.load(f)

with open(product_json_path) as f:
    motor_data = json.load(f)

# Extract the overall product description from the JSON
overall_motor_name = motor_data['description']

# Define flow properties (Assuming these properties exist in your openLCA database)
energy = client.find(o.FlowProperty, name="Energy")
items = client.find(o.FlowProperty, name="Number of items")

# Define units 
group_ref_items = client.find(o.UnitGroup, "Units of items")
group = client.get(o.UnitGroup, group_ref_items.id)
unit_items = [u for u in group.units if u.name == "Item(s)"]

group_ref_energy = client.find(o.UnitGroup, "Units of energy")
group = client.get(o.UnitGroup, group_ref_energy.id)
unit_kWh = [u for u in group.units if u.name == "kWh"]

# Initialize total power consumption
total_power_consumption = 0.0

# Calculate the total power consumption from procedure emissions
for procedure in procedure_data:
    # Ensure 'procedure_emission' exists and has 'power_consumption'
    if 'procedure_emission' in procedure and 'power_consumption' in procedure['procedure_emission']:
        power_consumption = procedure['procedure_emission']['power_consumption']
        total_power_consumption += power_consumption
    else:
        print(f"No power consumption data available for procedure: {procedure['id_short']}")

total_power_consumption = round(total_power_consumption, 4)
print(f"Total power consumption from all procedures: {total_power_consumption} kWh")

# Fetch the overall motor process object using its name
overall_process = client.get(o.Process, name=overall_motor_name)

# Fetch the full process object using its ID
print(f"Found process: {overall_process.name} with ID: {overall_process.id}")

# Retrieve existing exchanges
existing_exchanges = overall_process.exchanges if overall_process.exchanges else []

# Check if the power flow is already in the exchanges
power_flow_found = False

for exchange in existing_exchanges:
    if exchange.flow.id == "4f19a2f2-7b3b-11dd-ad8b-0800200c9a66" and exchange.is_input:
        # Update the existing power flow exchange amount
        exchange.amount = total_power_consumption
        power_flow_found = True
        print(f"Updated existing power flow: {exchange.flow.name} to new quantity: {total_power_consumption} kWh")
        break

if not power_flow_found:
    # If the power flow was not found in existing exchanges, add it as a new exchange
    power_flow = client.get(o.Flow, uid="4f19a2f2-7b3b-11dd-ad8b-0800200c9a66")
    if power_flow:
        power_exchange = o.Exchange()
        power_exchange.flow = power_flow
        power_exchange.amount = total_power_consumption
        power_exchange.unit = unit_kWh[0]
        power_exchange.is_input = True  # Indicate that this is an input exchange

        # Append the new input exchange to the list of existing exchanges
        existing_exchanges.append(power_exchange)

        print(f"Added new power flow: {power_flow.name} with quantity: {total_power_consumption} kWh")

# Update the overall motor process with the modified exchanges
overall_process.exchanges = existing_exchanges

# Put the updated process back into the database
client.put(overall_process)
print(f"All energy flows have been updated for the overall motor process: {overall_process.name}")

# Build Product System
# Check if a product system with the given name already exists
existing_product_system = client.find(o.ProductSystem, name=overall_motor_name)

if existing_product_system:
    print(f"Product system '{overall_motor_name}' already exists. No new product system will be created.")
    calculate_product_system = existing_product_system
else:
    # Create a linking configuration for the product system
    config = o.LinkingConfig(
        prefer_unit_processes=False,
        provider_linking=o.ProviderLinking.PREFER_DEFAULTS,
    )

    # Create the product system using the overall motor process as the root
    overall_product_system = client.create_product_system(overall_process, config)
    print(f"Created new product system: {overall_motor_name} with ID: {overall_product_system.id}")
    calculate_product_system = overall_product_system

# Conduct the actual LCA
# Select the impact method
impact_method = "83812f2a-8272-3244-91a5-20ca745f0902"

# create a calculation setup
setup = o.CalculationSetup(
    target=o.Ref(
        ref_type=o.RefType.ProductSystem,
        id= calculate_product_system.id,
    ),
    impact_method=o.Ref(id=impact_method),
    nw_set= None,
    amount= 1.0
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
            "Unit": impact_value.impact_category.ref_unit
        })
    df_total_impacts = pd.DataFrame(total_impacts_data)
    
   # Define the path to save the Excel file

    print(df_total_impacts)