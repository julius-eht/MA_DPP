import requests
import json
import os

# Define the base URL for the server
BASE_URL = "http://127.0.0.1:8000"

# Define the paths for each AAS type
PATHS = {
    "Product": "/Product/",
    "Process": "/Process/",
    "Procedure": "/Procedure/"
}

# Directory where JSON files are stored
JSON_DIRECTORY = "Stellmotor_Skript"  # Adjust this if your JSON files are in a different directory

# List of JSON files to post
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
    file_path = os.path.join(JSON_DIRECTORY, json_file)
    with open(file_path, 'r') as file:
        data = json.load(file)
        print(f"Posting JSON data to {url}: {json.dumps(data, indent=2)}")
        response = requests.post(url, json=data, allow_redirects=True)
        print(f"POST request to {url} with headers: {response.request.headers}")
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.content.decode()}")
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
        if result["status_code"] != 201 and result["status_code"] != 200:
            print(f"Failed to upload {result['file']}: {result['response']}")
        else:
            print(f"Successfully uploaded {result['file']}")

# Function to get JSON data
def get_json(url):
    response = requests.get(url, allow_redirects=True)
    print(f"GET request to {url} with headers: {response.request.headers}")
    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response content: {response.content.decode()}")
    response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
    return response.json()

# Extract and print all procedures
def extract_procedures():
    product_data = get_json(BASE_URL + PATHS["Product"] + "product_001")
    main_process_id = product_data["process_reference"]["process_id"]
    
    process_data = get_json(BASE_URL + PATHS["Process"] + f"{main_process_id}")
    attached_process_ids = process_data["process_model"]["sequence"]

    procedure_responses = []
    for process_id in attached_process_ids:
        print(f"Processing attached process ID: {process_id}")
        process_data = get_json(BASE_URL + PATHS["Process"] + f"{process_id}")
        
        process_attributes = process_data.get("process_attributes", {}).get("id_short")
        if process_attributes:
            procedure_id = f"procedure_{process_id.split('_', 1)[1]}"
            print(f"Derived procedure ID: {procedure_id}")
            procedure_url = BASE_URL + PATHS["Procedure"] + f"{procedure_id}"
            print(f"Attempting to GET procedure data from URL: {procedure_url}")
            procedure_data = get_json(procedure_url)
            procedure_responses.append(procedure_data)
        else:
            print(f"No process attributes found for process {process_id}")
    
    return procedure_responses

# Main execution
if __name__ == "__main__":
    # Post all JSONs
    post_results = post_all_jsons()

    # Check if all uploads were successful
    check_uploads(post_results)

    # Extract and print procedure data
    procedures = extract_procedures()
    print("Extracted procedure data:")
    print(json.dumps(procedures, indent=2))
