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
paint_seed = int(input("Enter the paint_seed value: "))

# Set the parameters with userinput values
params = {
    "paint_seed": paint_seed, 
    "paint_index": paint_index
}

headers = {
    "Authorization": api_key
}

response = requests.get(url, headers=headers, params=params)

# Print status code
print("Status Code:", response.status_code)

# Print the JSON response with pretty formatting
try:
    # Parse the JSON response and pretty print it
    json_data = response.json()
    print(json.dumps(json_data, indent=4, sort_keys=True))
except ValueError as e:
    print("Error parsing JSON:", e)
