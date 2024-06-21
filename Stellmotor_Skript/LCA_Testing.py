import json
import pandas as pd
import olca_ipc as ipc
import olca_schema as o
import uuid
from typing import Callable

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

group_ref_mass = client.find(o.UnitGroup, "Units of mass")
group = client.get(o.UnitGroup, group_ref_mass.id)
kg = [u for u in group.units if u.name == "kg"]

group_ref_items = client.find(o.UnitGroup, "Units of items")
group = client.get(o.UnitGroup, group_ref_items.id)
items = [u for u in group.units if u.name == "Item(s)"]

group_ref_energy = client.find(o.UnitGroup, "Units of energy")
group = client.get(o.UnitGroup, group_ref_energy.id)
kWh = [u for u in group.units if u.name == "kWh"]

print(kg, items, )