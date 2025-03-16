from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
# Access the API key from the environment variable
api_key = os.getenv("CSFLOAT_API_KEY")
if not api_key:
    raise ValueError("API key not found in .env file. Please create a .env file with CSFLOAT_API_KEY.")

url = "https://csfloat.com/api/v1/listings"

# Prompt user to choose between simple and detailed search
search_mode = input("Choose search mode (simple/detailed) [default: simple]: ").strip().lower()
if search_mode not in ["simple", "detailed"]:
    search_mode = "simple"  

# Get paint_index value from user
paint_index = int(input("Enter the paint_index value: "))    

# Get list of paint_seeds from user
user_input = input("Enter a list of paint_seed values (comma-separated): ")

# Convert the user input into a list of integers
paint_seeds = [int(seed.strip()) for seed in user_input.split(",")]

# Prompt user for additional parameters
additional_params = input("Any additional parameters? (e.g., max_price: 100, min_price: 50, max_float: 0.07, min_float: 0.56): ").strip()

# Parse the additional parameters
params = {
    "paint_seed": None,
    "paint_index": paint_index
}

# Add additional parameters if provided
if additional_params:
    for param in additional_params.split(","):
        # Split the parameter into key and value
        param = param.strip()
        if ":" in param:
            key, value = param.split(":", 1) 
            key = key.strip()
            value = value.strip()

            # Convert value to the appropriate type
            if key in ["max_price", "min_price"]:
                value = int(value) * 100  
            elif key in ["max_float", "min_float"]:
                # Replace commas with periods for float values
                value = float(value.replace(",", "."))

            params[key] = value
        else:
            print(f"Warning: Skipping invalid parameter '{param}'. Expected format 'key: value'.")

# Define the headers with the API key for Authorization
headers = {
    "Authorization": api_key
}

# Loop through the list of paint_seed values and send a GET request for each
for paint_seed in paint_seeds:
    params["paint_seed"] = paint_seed 

    response = requests.get(url, headers=headers, params=params)

    # If the response is successful (status code 200), process the JSON data
    if response.status_code == 200:
        try:
            # Parse the JSON response
            json_data = response.json()

            # Initialize a set to store unique ids
            unique_ids = set()

            # Check if the response contains the 'data' key
            if 'data' in json_data and isinstance(json_data['data'], list):
                # Iterate over the 'data' array
                for item in json_data['data']:
                    if 'id' in item:  # Check if 'id' is in the item
                        unique_ids.add(item['id'])

                        # If detailed search mode, print all details of the item
                        if search_mode == "detailed":
                            print(json.dumps(item, indent=2))  # Pretty-print the item details

                # Count of unique ids
                count = len(unique_ids)

                # Print the number of unique ids for this paint_seed
                print(f"Unique listings for paint_seed {paint_seed}: {count}")
            else:
                print(f"No data found for paint_seed {paint_seed}.")
        except ValueError as e:
            print(f"Error parsing JSON for paint_seed {paint_seed}: {e}")
    else:
        print(f"Failed to fetch data for paint_seed {paint_seed}")

    # Add a separator for readability between responses
    print("\n" + "-"*80 + "\n")