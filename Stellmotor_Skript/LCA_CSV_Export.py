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

# Process the JSON data
# Process the BOM and gather component data
bom = passport_data.get('bom', {}).get('sub_products', [])
for sub_product in bom:
    sub_product_id = sub_product.get('passport_id')
    sub_product_quantity = sub_product.get('quantity', 1)
    sub_product_target_PCF = passport_id + (' PCF')
    sub_product_target_TCF = passport_id + (' TCF')

    # Get component data
    component_data = Method_Toolbox.get_json(BASE_URL + PATHS["Passport"] + f"{sub_product_id}")
    component_footprint_data = component_data.get('carbon_footprint')

    # Process PCF data for component
    for footprint in component_footprint_data.get('product_footprints', []):
        pcf_data.append({
            'Source': sub_product_id,
            'Target': sub_product_target_PCF,
            'Value': footprint.get('PCFCO2eq', 0) * sub_product_quantity
        })

    # Process TCF data for component
    for footprint in component_footprint_data.get('transport_footprints', []):
        tcf_data.append({
            'Source': sub_product_id,
            'Target': sub_product_target_TCF,
            'Value': footprint.get('TCFCO2eq', 0) * sub_product_quantity
        })

# Calculate Remaining Emission on the OEM Level (Assumption: Total - Components)
pcf_co2eq_value = None
if 'carbon_footprint' in passport_data:
    if 'product_footprints' in passport_data['carbon_footprint']:
        for product_footprint in passport_data['carbon_footprint']['product_footprints']:
            if 'PCFCO2eq' in product_footprint:
                pcf_co2eq_value = product_footprint['PCFCO2eq']
                break
            else:
                print("PCFCO2eq key not found in product_footprint:", product_footprint)
    else:
        print("product_footprints key not found in carbon_footprint:", passport_data['carbon_footprint'])
else:
    print("carbon_footprint key not found in data:", passport_data)

tcf_co2eq_value = None
if 'carbon_footprint' in passport_data:
    if 'transport_footprints' in passport_data['carbon_footprint']:
        for transport_footprint in passport_data['carbon_footprint']['transport_footprints']:
            if 'TCFCO2eq' in transport_footprint:
                tcf_co2eq_value = transport_footprint['TCFCO2eq']
                break
            else:
                print("TCFCO2eq key not found in transport_footprint:", transport_footprint)
    else:
        print("transport_footprints key not found in carbon_footprint:", passport_data['carbon_footprint'])
else:
    print("carbon_footprint key not found in data:", passport_data)

OEM_PCF_Contribution = pcf_co2eq_value - sum(item['Value'] for item in pcf_data) 
OEM_TCF_Contribution = tcf_co2eq_value - sum(item['Value'] for item in tcf_data) 


# Append OEM Information
pcf_data.append({
    'Source': "OEM",
    'Target': sub_product_target_PCF,
    'Value': OEM_PCF_Contribution
        })

tcf_data.append({
    'Source': "OEM",
    'Target': sub_product_target_TCF,
    'Value': OEM_TCF_Contribution
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
