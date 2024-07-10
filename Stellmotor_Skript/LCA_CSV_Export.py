import json
import csv
import requests
import Method_Toolbox

# Define the base URL for the server
BASE_URL = "http://127.0.0.1:8000"

# Define the paths for each AAS type
PATHS = {
    "Product": "/Product/",
    "Process": "/Process/",
    "Procedure": "/Procedure/",
    "Passport": "/Passport/"
}

passport_id = "motor_passport_001"
passport_data = Method_Toolbox.get_json(BASE_URL + PATHS["Passport"] + f"{passport_id}")

# Initialize lists to store PCF and TCF data
pcf_data = []
tcf_data = []
other_data = []

footprint_data =passport_data.get('carbon_footprint')

# Process the JSON data
# Process the BOM and gather component data
bom = passport_data.get('bom', {}).get('sub_products', [])
for sub_product in bom:
    sub_product_id = sub_product.get('passport_id')
    sub_product_quantity = sub_product.get('quantity', 1)
    sub_product_target_PCF = passport_id + ('PCF')
    sub_product_target_TCF = passport_id + ('TCF')

    # Get component data
    component_data = Method_Toolbox.get_json(BASE_URL + PATHS["Passport"] + f"{sub_product_id}")
    print(component_data)
    component_footprint_data = component_data.get('carbon_footprint')

    # Process PCF data for component
    for footprint in component_footprint_data.get('product_footprints', []):
        pcf_data.append({
            'Source': "Supplier",
            'Target': sub_product_target_PCF,
            'Value': footprint.get('PCFCO2eq', 0) * sub_product_quantity
        })

    # Process TCF data for component
    for footprint in component_footprint_data.get('transport_footprints', []):
        tcf_data.append({
            'Source': "Supplier",
            'Target': sub_product_target_PCF,
            'Value': footprint.get('TCFCO2eq', 0) * sub_product_quantity
        })


# Combine all data for the final CSV
final_data = pcf_data + tcf_data + other_data

# Define the CSV file path
csv_file_path = 'Stellmotor_Skript/Output/carbon_footprint_data.csv'

# Write the data to a CSV file
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['Source', 'Target', 'Value']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in final_data:
        writer.writerow(row)

print(f'Data successfully written to {csv_file_path}')
