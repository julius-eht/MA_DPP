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

# Initialize the IPC client for openLCA
client = ipc.Client(8083)

# Load the product information from the Server file and procedure information from the file

product_id = "product_001" # Adjust using User Input

motor_data = Method_Toolbox.get_json(BASE_URL + PATHS["Product"] + f"{product_id}")

# Load Procedure data from SDM Model for Power Consumption Calculation
procedure_data = Method_Toolbox.retrieve_attached_procedures(product_id)
print(f"Retrieved procedure data for {product_id}")

# Extract the overall product description from the JSON
overall_motor_name = motor_data['id_short']

# Define units 
group_ref_items = client.find(o.UnitGroup, "Units of items")
group = client.get(o.UnitGroup, group_ref_items.id)
unit_items = [u for u in group.units if u.name == "Item(s)"]

group_ref_energy = client.find(o.UnitGroup, "Units of energy")
group = client.get(o.UnitGroup, group_ref_energy.id)
unit_kWh = [u for u in group.units if u.name == "kWh"]

group_ref_transport = client.find(o.UnitGroup, "Units of mass*length")
group = client.get(o.UnitGroup, group_ref_transport.id)
unit_transport = [u for u in group.units if u.name == "t*km"]

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

# Fetch Auxillary Information
aux_excel_path = r'C:\Users\juliu\OneDrive\Dokumente\GitHub\MA_DPP\Stellmotor_Skript\Input_Files\24-06-20_Supplementary Excel.xlsx' # Change Excel path if necessary
aux_data = pd.read_excel(aux_excel_path, sheet_name="SUPP_INFO")
electricity_flow_id = aux_data.loc[aux_data['descr'] == 'Electricity', 'Flow ID'].values[0]
electricity_provider_id = aux_data.loc[aux_data['descr'] == 'Electricity', 'Provider ID'].values[0]
transport_flow_id = aux_data.loc[aux_data['descr'] == 'Transport', 'Flow ID'].values[0]
transport_provider_id = aux_data.loc[aux_data['descr'] == 'Transport', 'Provider ID'].values[0]
transport_value = aux_data.loc[aux_data['descr'] == 'Transport', 'Amount'].values[0]
impact_method_id = aux_data.loc[aux_data['descr'] == 'ImpactMethod', 'Flow ID'].values[0]

# Fetch the overall motor process object using its name
overall_process = client.get(o.Process, name=overall_motor_name)

# Fetch the auxillary processes for the provision in the overall product system process
electricity_provider = client.get(o.Process, uid=electricity_provider_id)
transport_provider = client.get(o.Process, uid=transport_provider_id)

# Fetch the full process object using its ID
print(f"Found process: {overall_process.name} with ID: {overall_process.id}")

# Retrieve existing exchanges
existing_exchanges = overall_process.exchanges if overall_process.exchanges else []

# Check if the transport flow is already in the exchanges
transport_flow_found = False

for exchange in existing_exchanges:
    if exchange.flow.id == transport_flow_id and exchange.is_input:
        # Update the existing transport flow exchange amount
        exchange.amount = transport_value
        transport_flow_found = True
        print(f"Updated existing transport flow: {exchange.flow.name} to new value: {transport_value} t*km")
        break

if not transport_flow_found:
    # If the transport flow was not found in existing exchanges, add it as a new exchange
    transport_flow = client.get(o.Flow, uid=transport_flow_id)
    if transport_flow:
        transport_exchange = o.Exchange()
        transport_exchange.flow = transport_flow
        transport_exchange.amount = transport_value
        transport_exchange.unit = unit_transport[0]
        transport_exchange.is_input = True  # Indicate that this is an input exchange
        transport_exchange.default_provider = transport_provider

        # Append the new input exchange to the list of existing exchanges
        existing_exchanges.append(transport_exchange)

        print(f"Added new transport flow: {transport_flow.name} with value: {transport_value} t*km")

# Check if the power flow is already in the exchanges
power_flow_found = False

for exchange in existing_exchanges:
    if exchange.flow.id == electricity_flow_id and exchange.is_input:
        # Update the existing power flow exchange amount
        exchange.amount = total_power_consumption
        power_flow_found = True
        print(f"Updated existing power flow: {exchange.flow.name} to new quantity: {total_power_consumption} kWh")
        break

if not power_flow_found:
    # If the power flow was not found in existing exchanges, add it as a new exchange
    power_flow = client.get(o.Flow, uid=electricity_flow_id)
    if power_flow:
        power_exchange = o.Exchange()
        power_exchange.flow = power_flow
        power_exchange.amount = total_power_consumption
        power_exchange.unit = unit_kWh[0]
        power_exchange.is_input = True  # Indicate that this is an input exchange
        power_exchange.default_provider = electricity_provider

        # Append the new input exchange to the list of existing exchanges
        existing_exchanges.append(power_exchange)

        print(f"Added new power flow: {power_flow.name} with quantity: {total_power_consumption} kWh")

# Update the overall motor process with the modified exchanges
overall_process.exchanges = existing_exchanges

# Put the updated process back into the database
client.put(overall_process)
print(f"All energy and transport flows have been updated for the overall motor process: {overall_process.name}")

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
        provider_linking=o.ProviderLinking.ONLY_DEFAULTS,
    )
    # Create the product system using the overall motor process as the root
    overall_product_system = client.create_product_system(overall_process, config)
    print(f"Created new product system: {overall_motor_name} with ID: {overall_product_system.id}")
    calculate_product_system = overall_product_system

# Conduct the actual LCA
# Select the impact method
impact_method = impact_method_id 

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

# Check for errors
if result.error:
    print(f"Error during calculation: {result.error}")

impact_category = client.find(o.ImpactCategory, name="IPCC GWP 100a")

tech_flows = result.get_tech_flows()
filtered_impacts = []

for tech_flow in tech_flows:
    provider_name = tech_flow.provider.name
    direct_impacts = result.get_direct_impacts_of(tech_flow)
    for impact in direct_impacts:
        if impact.amount > 0:
            filtered_impacts.append((provider_name, impact.amount))
            
# Display the filtered impacts
print("Results of the LCA:")
for provider_name, amount in filtered_impacts:
    print(f"{provider_name}: {amount} kg CO2 eq")

# Define the name of the transport process
transport_process_name = "Lorry transport, Euro 0, 1, 2, 3, 4 mix, 22 t total weight, 17,3t max payload"

# Extract the CO2 value for the transport process using defined funtion
def get_co2_values(filtered_impacts, exclude_process_name):
    exclude_process_co2_value = None
    other_co2_sum = 0.0

    for provider_name, co2_value in filtered_impacts:
        if provider_name == exclude_process_name:
            exclude_process_co2_value = co2_value
        else:
            other_co2_sum += co2_value

    return exclude_process_co2_value, other_co2_sum

transport_co2_value, production_co2_sum = get_co2_values(filtered_impacts, transport_process_name)

# Identify the Overall PCF
motor_passport_name = motor_data['product_information']['passport_id']

# Calculate Total PCF and TCF
component_pcf = Method_Toolbox.retrieve_total_pcf(motor_passport_name)
component_tcf = Method_Toolbox.retrieve_total_tcf(motor_passport_name)
total_pcf = component_pcf + production_co2_sum
total_tcf = component_tcf + transport_co2_value

#Print Results
print(f"The total components account for {component_pcf} kg CO2eq in Production")
print(f"The total components account for {component_tcf} kg CO2eq in Transport")
print(f"The OEM accounts for {production_co2_sum} kg CO2eq in Production")
print(f"The OEM accounts for {transport_co2_value} kg CO2eq in Transport")

#Upload Results
Method_Toolbox.update_passport_with_pcf(motor_passport_name,total_pcf,0)
Method_Toolbox.update_passport_with_tcf(motor_passport_name,total_tcf,0)
print('Updated TCF and PCF of the product system, script execution complete.')