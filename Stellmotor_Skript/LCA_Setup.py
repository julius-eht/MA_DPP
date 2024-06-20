import json
import pandas as pd
import olca
from olca import ipc

# Step 1: Load input data from JSON files
product_json_path =  "AAS_motor_example.json"  # Update this path to the actual JSON file path
power_input_json_path = '/mnt/data/Procedure_Classes.json'  # Path to the JSON file with power input information

# Load product data
with open(product_json_path) as file:
    product_data = json.load(file)

# Load power input data
with open(power_input_json_path) as file:
    power_input_data = json.load(file)

# Step 2: Load BOM details including weights and material types from an Excel file
bom_excel_path = '/mnt/data/BOM_Details_Input.xlsx'  # Update this path to the actual Excel file path
bom_df = pd.read_excel(bom_excel_path)

print(f"Loaded BOM details from {bom_excel_path}")

# Display the loaded BOM details
print(bom_df)

# Extracting BOM information
bom = bom_df.to_dict('records')

# Step 3: Extract and sum up power consumption from procedures

# Initialize total power consumption
total_power_consumption = 0.0

# Assume power_input_data is a list of procedures each containing a 'power_consumption' field
for procedure in power_input_data.get('procedures', []):
    power_consumption = procedure.get('power_consumption', 0.0)
    total_power_consumption += power_consumption

print(f"Total power consumption from all procedures: {total_power_consumption} kWh")

# Step 4: Set up OpenLCA OLCA Interface

# Connect to OpenLCA using the client
client = ipc.Client(8080)  # Assuming the default port for OpenLCA

# Function to create a flow in OpenLCA
def create_flow(name, unit, category):
    flow = olca.Flow()
    flow.name = name
    flow.flow_type = olca.FlowType.PRODUCT_FLOW
    flow.unit_group = client.get(olca.UnitGroup, client.find(olca.UnitGroup, unit)[0])
    flow.flow_properties = [{
        "flow_property": client.get(olca.FlowProperty, client.find(olca.FlowProperty, "Mass")[0]),
        "unit": client.get(olca.Unit, client.find(olca.Unit, "Kilogram")[0]),
        "quantitative_reference": True
    }]
    flow.category = client.get(olca.Category, client.find(olca.Category, category)[0])
    client.insert(flow)
    return flow

# Function to create a product system in OpenLCA
def create_product_system(flow, name):
    product_system = olca.ProductSystem()
    product_system.name = name
    product_system.reference_flow_property = flow.flow_properties[0]['flow_property']
    product_system.reference_unit = flow.flow_properties[0]['unit']
    product_system.reference_process = None  # Will be set later
    product_system.target_unit = flow.flow_properties[0]['unit']
    client.insert(product_system)
    return product_system

# Step 5: Create flows and product systems for individual components using BOM data
for component in bom:
    description = component['description']
    weight = component['material_weight']
    material_type = component['material_type']
    
    flow = create_flow(description, "Mass", "Components")
    product_system = create_product_system(flow, description)
    print(f"Created flow and product system for: {description}, Weight: {weight}, Material: {material_type}")

# Step 6: Create flow and product system for the overall product
overall_flow = create_flow("Bosch AHC2 Motor", "Mass", "Overall Product")
overall_product_system = create_product_system(overall_flow, "Bosch AHC2 Motor")

# Aggregating the quantities for the overall product system
for component in bom:
    description = component['description']
    quantity = component['quantity']
    flow = client.get(olca.Flow, client.find(olca.Flow, description)[0])
    client.add_flow_to_product_system(overall_product_system, flow, quantity)

# Adding the total power input as a flow (assuming it's in kWh)
power_flow = create_flow("Power Input", "Energy", "Energy Inputs")
client.add_flow_to_product_system(overall_product_system, power_flow, total_power_consumption)

print("Added total power input to the overall product system.")

# Step 7: Run the LCA using ReCiPe 2016 Midpoint (H) method

# Define the impact method
impact_method = client.get(olca.ImpactMethod, client.find(olca.ImpactMethod, "ReCiPe 2016 Midpoint (H)")[0])

# Run LCA for each product system
lca_results = {}
for component in bom:
    description = component['description']
    product_system = client.get(olca.ProductSystem, client.find(olca.ProductSystem, description)[0])
    lca_result = client.calculate_lca(product_system, impact_method)
    lca_results[description] = lca_result
    print(f"LCA result for {description}: {lca_result}")

# Run LCA for the overall product system
overall_product_system_id = client.find(olca.ProductSystem, "Bosch AHC2 Motor")[0]
overall_product_system = client.get(olca.ProductSystem, overall_product_system_id)
overall_lca_result = client.calculate_lca(overall_product_system, impact_method)
lca_results["Bosch AHC2 Motor"] = overall_lca_result
print(f"Overall LCA result for Bosch AHC2 Motor: {overall_lca_result}")

# Save LCA results to a file
lca_results_path = '/mnt/data/LCA_Results.xlsx'
with pd.ExcelWriter(lca_results_path) as writer:
    for component, result in lca_results.items():
        lca_result_df = pd.DataFrame([result])
        lca_result_df.to_excel(writer, sheet_name=component)

print(f"LCA results saved to {lca_results_path}")

# Close the OpenLCA client connection
client.close()
