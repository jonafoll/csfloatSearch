from dotenv import load_dotenv
import os
import requests
import json
import time

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

# Get def_index value from user
def_index = int(input("Enter the def_index value: "))    

# Get list of paint_seeds from user
user_input = input("Enter a list of paint_seed values (comma- or space-separated): ")

# Replace spaces with commas and split into a list
if " " in user_input:
    user_input = user_input.replace(" ", ",")  # Replace spaces with commas

# Convert the user input into a list of integers
paint_seeds = [int(seed.strip()) for seed in user_input.split(",")]

# Prompt the user for additional parameters
additional_params = input("Any additional parameters? (e.g., max_price: 100, min_price: 50, max_float: 0.5): ").strip()

# Parse the additional parameters
params = {
    "def_index": def_index,  # Permanent def_index
    "paint_index": paint_index,  # Permanent paint_index
}

# Add additional parameters if provided
if additional_params:
    for param in additional_params.split(","):
        # Split the parameter into key and value
        param = param.strip()
        if ":" in param:
            key, value = param.split(":", 1)  # Split on the first colon only
            key = key.strip()
            value = value.strip()

            # Convert value to the appropriate type
            if key in ["max_price", "min_price"]:
                value = int(value) * 100  # Convert USD to cents
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

# Send the GET request to fetch all listings for the given def_index and paint_index
response = requests.get(url, headers=headers, params=params)

# If the response is successful (status code 200), process the JSON data
if response.status_code == 200:
    try:
        # Parse the JSON response
        json_data = response.json()

        # Check if the response contains the 'data' key
        if 'data' in json_data and isinstance(json_data['data'], list):
            # Initialize a dictionary to store counts for each paint_seed
            seed_counts = {seed: 0 for seed in paint_seeds}

            # Iterate over the listings and count matches for each paint_seed
            for item in json_data['data']:
                item_seed = item.get("item", {}).get("paint_seed")
                if item_seed in seed_counts:
                    seed_counts[item_seed] += 1

                    # If detailed search mode, print all details of the item
                    if search_mode == "detailed":
                        print(json.dumps(item, indent=2))  # Pretty-print the item details

            # Print the count of listings for each paint_seed (only if count > 0)
            for seed, count in seed_counts.items():
                if count > 0:
                    print(f"Unique listings for paint_seed {seed}: {count}")

            # Print the total count of unique listings (always print, even if 0)
            total_count = sum(seed_counts.values())
            print(f"Total unique listings for all seeds: {total_count}")
        else:
            print(f"No data found for def_index {def_index} and paint_index {paint_index}.")
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
elif response.status_code == 429:
    # Handle rate limiting
    retry_after = int(response.headers.get("Retry-After", 5))  # Default to 5 seconds if Retry-After header is missing
    print(f"Rate limit exceeded. Waiting for {retry_after} seconds before retrying...")
    time.sleep(retry_after)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")