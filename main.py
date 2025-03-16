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

# Get user input for paint_index and paint_seed
paint_index = int(input("Enter the paint_index value: "))

# Get user input for paint_seed in a list
user_input = input("Enter a list of paint_seed values (comma-separated): ")
paint_seeds = [int(seed.strip()) for seed in user_input.split(",")]

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

    print(f"Status Code for paint_seed {paint_seed}:", response.status_code)

    if response.status_code == 200:
        try:
            json_data = response.json()
            print(f"Response for paint_seed {paint_seed}:")
            print(json.dumps(json_data, indent=4, sort_keys=True))
        except ValueError as e:
            print(f"Error parsing JSON for paint_seed {paint_seed}: {e}")
    else:
        print(f"Failed to fetch data for paint_seed {paint_seed}")
    
    print("\n" + "-"*80 + "\n")