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

# Headers to match manual upload (Postman)
headers = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "User-Agent": "PostmanRuntime/7.39.0"  # This mirrors the User-Agent from the manual upload
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

]

# Function to post JSON data
def post_json(json_file, path):
    url = BASE_URL + path
    file_path = os.path.join(JSON_DIRECTORY, json_file)
    with open(file_path, 'r') as file:
        data = json.load(file)
        response = requests.post(url, json=data,headers=headers, allow_redirects=True) 
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
        if result["status_code"] != 201 and result["status_code"] != 200:  # Including 200 as a success status code
            print(f"Failed to upload {result['file']}: {result['response']}")
        else:
            print(f"Successfully uploaded {result['file']}")

# Retrieve all attached procedures for a given product
def retrieve_attached_procedures(product_id):
    procedure_responses = []

    # Function to get JSON data from the server
    def get_json(url):
        print(f"Attempting to GET data from URL: {url}")  # Debug line to print the exact URL being requested
        response = requests.get(url, allow_redirects=True)  # Allowing redirects
        print(f"Response status code: {response.status_code}")  # Debug line to show status code
        if response.status_code != 200:
            print(f"Error {response.status_code} for URL: {url}")
            print(f"Response headers: {response.headers}")  # Print response headers
            print(f"Response content: {response.text}")  # Print response content
            response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        return response.json()

    # Load the product AAS to find the main process
    try:
        product_data = get_json(BASE_URL + PATHS["Product"] + f"{product_id}")
        print(f"Retrieved product data for {product_id}")
        main_process_id = product_data.get("process_reference", {}).get("process_id")
        if not main_process_id:
            print(f"Main process not found for product {product_id}")
            return procedure_responses
        print(f"Main process ID found: {main_process_id}")
    except Exception as e:
        print(f"Failed to get product data for {product_id}: {e}")
        return procedure_responses

    # Load the main process to find attached processes
    try:
        main_process_data = get_json(BASE_URL + PATHS["Process"] + f"{main_process_id}")
        print(f"Retrieved main process data for {main_process_id}")
        attached_process_ids = main_process_data.get("process_model", {}).get("sequence", [])
        print(f"Attached process IDs found: {attached_process_ids}")
    except Exception as e:
        print(f"Failed to get main process data for {main_process_id}: {e}")
        return procedure_responses

    # Retrieve procedure data for each attached process using process attributes
    for process_id in attached_process_ids:
        try:
            print(f"Processing attached process ID: {process_id}")
            # Fetch the process data to get the process attributes
            process_data = get_json(BASE_URL + PATHS["Process"] + f"{process_id}")
            process_attributes = process_data.get("process_attributes", {}).get("id_short")
            if process_attributes:
                # Derive the procedure ID from the process ID
                procedure_id = f"procedure_{process_id.split('_', 1)[1]}"
                print(f"Derived procedure ID: {procedure_id}")
                # Construct the full URL for the procedure
                procedure_url = BASE_URL + PATHS["Procedure"] + f"{procedure_id}"
                print(f"Attempting to GET procedure data from URL: {procedure_url}")  # Debug line to print procedure URL
                # Fetch the procedure data using the derived procedure ID
                procedure_data = get_json(procedure_url)
                print(f"Retrieved procedure data for {procedure_id}")
                procedure_responses.append(procedure_data)
            else:
                print(f"No process attributes found for process {process_id}")
        except Exception as e:
            print(f"Failed to get procedure data for {process_id}: {e}")

    print("Completed retrieval of all attached procedures.")
    return procedure_responses


# Save the retrieved procedure data to a JSON file
def save_procedures(data, file_path="attached_procedures.json"):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Attached procedures data saved to {file_path}")

# Main execution
if __name__ == "__main__":
    # Post all JSONs
    post_results = post_all_jsons()

    # Check if all uploads were successful
    check_uploads(post_results)
    """
    # Retrieve attached procedures for the given product
    product_id = "product_001"  # Adjust to your product ID
    attached_procedures_data = retrieve_attached_procedures(product_id)
    

    # Save the attached procedures data to a file
    if attached_procedures_data:
        save_procedures(attached_procedures_data)

    print("Script execution completed.")

    """