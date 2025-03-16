from dotenv import load_dotenv
import os
import requests
import json

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
api_key = os.getenv("CSFLOAT_API_KEY")
if not api_key:
    raise ValueError("API key not found in .env file. Please create a .env file with CSFLOAT_API_KEY.")

url = "https://csfloat.com/api/v1/listings"

# Prompt user to choose between simple and detailed search
search_mode = input("Choose search mode (simple/detailed) [default: simple]: ").strip().lower()
if search_mode not in ["simple", "detailed"]:
    search_mode = "simple"  # Default to simple if invalid or no input is provided

# Get paint_index value from user
paint_index = int(input("Enter the paint_index value: "))    

# Get list of paint_seeds from user
user_input = input("Enter a list of paint_seed values (comma-separated): ")

# Convert the user input into a list of integers
paint_seeds = [int(seed.strip()) for seed in user_input.split(",")]


# Define headers with the API key for Authorization
headers = {
    "Authorization": api_key
}

# Loop through the list of paint_seed values and send a GET request for each
for paint_seed in paint_seeds:
    params = {
        "paint_seed": paint_seed,
        "paint_index": paint_index
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        try:
            json_data = response.json()

            unique_ids = set()

            # Check if the response contains the 'data' key
            if 'data' in json_data and isinstance(json_data['data'], list):
                for item in json_data['data']:
                    if 'id' in item:  
                        unique_ids.add(item['id'])

                        # If detailed search mode, print all details of the item
                        if search_mode == "detailed":
                            print(json.dumps(item, indent=2)) 

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

    print("\n" + "-"*80 + "\n")