import requests
import json
import os

# Define the base URL for the server
BASE_URL = "http://127.0.0.1:8000"

# Define the paths for each AAS type
PATHS = {
    "Product": "/Product/",
    "Process": "/Process/",
    "Procedure": "/Procedure/",
    "Passport": "/Passport/"
}

# Directory where JSON files are stored
JSON_DIRECTORY = "Stellmotor_Skript"  # Adjust this if  JSON files are in a different directory

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
    "Input_Files/Passport_motor_example.json",
    "Input_Files/AAS_motor_example.json",
    "Input_Files/AAS_process_pressen_1.json",
    "Input_Files/AAS_process_pressen_2_3.json",
    "Input_Files/AAS_process_pressen_4.json",
    "Input_Files/AAS_process_magnetisieren.json",
    "Input_Files/AAS_process_fugen_1.json",
    "Input_Files/AAS_process_fugen_2.json",
    "Input_Files/AAS_process_schrauben_1.json",
    "Input_Files/AAS_process_schrauben_2.json",
    "Input_Files/AAS_procedure_pressen_1.json",
    "Input_Files/AAS_procedure_pressen_4.json",
    "Input_Files/AAS_procedure_pressen_2_3.json",
    "Input_Files/AAS_procedure_magnetisieren.json",
    "Input_Files/AAS_procedure_fugen_1.json",
    "Input_Files/AAS_procedure_fugen_2.json",
    "Input_Files/AAS_procedure_schrauben_1.json",
    "Input_Files/AAS_procedure_schrauben_2.json",
    "Input_Files/Sub_AAS_anchor_example.json",
    "Input_Files/Sub_AAS_brushcarrier_example.json",
    "Input_Files/Sub_AAS_clamps_example.json",
    "Input_Files/Sub_AAS_geara_example.json",
    "Input_Files/Sub_AAS_gearb_example.json",
    "Input_Files/Sub_AAS_housingea_example.json",
    "Input_Files/Sub_AAS_housingeb_example.json",
    "Input_Files/Sub_AAS_magnethalves_example.json",
    "Input_Files/Sub_AAS_plasticpart_example.json",
    "Input_Files/Sub_AAS_poltopf_example.json",
    "Input_Files/Sub_AAS_ringmagnet_example.json",
    "Input_Files/Sub_AAS_screws_example.json",
    "Input_Files/Sub_AAS_wormwheel_example.json",
    "Input_Files/Passport_anchor_example.json",
    "Input_Files/Passport_brushcarrier_example.json",
    "Input_Files/Passport_clamps_example.json",
    "Input_Files/Passport_geara_example.json",
    "Input_Files/Passport_gearb_example.json",
    "Input_Files/Passport_grease_example.json",
    "Input_Files/Passport_housingea_example.json",
    "Input_Files/Passport_housingeb_example.json",
    "Input_Files/Passport_magnethalves_example.json",
    "Input_Files/Passport_plasticpart_example.json",
    "Input_Files/Passport_poltopf_example.json",
    "Input_Files/Passport_ringmagnet_example.json",
    "Input_Files/Passport_screws_example.json",
    "Input_Files/Passport_wormwheel_example.json"
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
    print("Uploading JSON files...")
    results = []
    for json_file in JSON_FILES:
        # Determine the path based on the JSON file name
        if "Passport" in json_file:
            path = PATHS["Passport"]
        elif "motor" in json_file:
            path = PATHS["Product"]
        elif "Sub_" in json_file:
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


# Main execution
if __name__ == "__main__":
    # Post all JSONs
    post_results = post_all_jsons()

    # Check if all uploads were successful
    check_uploads(post_results)

    print("AAS uploads completed.")
