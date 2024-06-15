import requests
import json
import os

# Define the base URL for the server
BASE_URL = "http://127.0.0.1:8000"

# Define the paths for each AAS type
PATHS = {
    "Product": "/Product",
    "Process": "/Process",
    "Procedure": "/Procedure"
}

# List of JSON files with corrected names to post
JSON_FILES = [
    "AAS_motor_example.json",
    "AAS_process_pressen_1.json",
    "AAS_process_pressen_2_3.json",
    "AAS_process_pressen_4.json",
    "AAS_process_magnetisieren.json",
    "AAS_process_fugen_1.json",
    "AAS_process_fugen_2.json",
    "AAS_process_schrauben_1.json",
    "AAS_process_schrauben_2.json",
    "AAS_procedure_pressen_1.json",
    "AAS_procedure_pressen_2_3.json",
    "AAS_procedure_pressen_4.json",
    "AAS_procedure_magnetisieren.json",
    "AAS_procedure_fugen_1.json",
    "AAS_procedure_fugen_2.json",
    "AAS_procedure_schrauben_1.json",
    "AAS_procedure_schrauben_2.json"
]

# Function to post JSON data
def post_json(json_file, path):
    url = BASE_URL + path
    with open(json_file, 'r') as file:
        data = json.load(file)
        response = requests.post(url, json=data)
        return response.status_code, response.json()

# Post all JSON files
def post_all_jsons():
    results = []
    for json_file in JSON_FILES:
        # Determine the path based on the JSON file name
        if "motor" in json_file:
            path = PATHS["Product"]
        elif "process" in json_file:
            path = PATHS["Process"]
        elif "procedure" in json_file:
            path = PATHS["Procedure"]
        else:
            continue
        status_code, response = post_json(json_file, path)
        results.append({
            "file": json_file,
            "status_code": status_code,
            "response": response
        })
    return results

# Check if uploads worked
def check_uploads(results):
    for result in results:
        if result["status_code"] != 201:  # Assuming 201 is the successful creation status code
            print(f"Failed to upload {result['file']}: {result['response']}")
        else:
            print(f"Successfully uploaded {result['file']}")

# Extract power consumption from procedures using GET requests
def extract_power_consumption():
    power_consumption_list = []

    # Function to get JSON data from the server
    def get_json(url):
        response = requests.get(url)
        return response.json()

    # Load the main product AAS to find the main process
    product_data = get_json(BASE_URL + PATHS["Product"] + "/AAS_motor_example")
    main_process_id = "process_pressen_2_3"  # Assuming the main process is known

    # Function to extract power consumption from a procedure
    def get_procedure_power_consumption(procedure_id):
        url = BASE_URL + PATHS["Procedure"] + f"/{procedure_id}"
        data = get_json(url)
        return {
            "procedure_id": data["id"],
            "description": data["description"],
            "id_short": data["id_short"],
            "semantic_id": data["semantic_id"],
            "power_consumption_kwh": data["procedure_emission"]["power_consumption"]
        }

    # Define the process sequence based on the main process model
    process_sequence = [
        "process_pressen_1",
        "process_pressen_2_3",
        "process_pressen_4",
        "process_magnetisieren",
        "process_fugen_1",
        "process_schrauben_1",
        "process_fugen_2",
        "process_schrauben_2"
    ]

    # Extract power consumption for each process in the sequence
    for process_id in process_sequence:
        procedure_data = get_procedure_power_consumption(process_id)
        if procedure_data:
            power_consumption_list.append(procedure_data)

    return power_consumption_list

# Save the power consumption data to a JSON file
def save_power_consumption(data, file_path="power_consumption.json"):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Power consumption data saved to {file_path}")

# Main execution
if __name__ == "__main__":
    # Post all JSONs
    post_results = post_all_jsons()

    # Check if all uploads were successful
    check_uploads(post_results)

    # Extract power consumption data
    power_consumption_data = extract_power_consumption()

    # Save the power consumption data to a file
    save_power_consumption(power_consumption_data)
