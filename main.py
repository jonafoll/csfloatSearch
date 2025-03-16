from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
api_key = os.getenv("CSFLOAT_API_KEY")
if not api_key:
    raise ValueError("API key not found in .env file. Please create a .env file with CSFLOAT_API_KEY.")

url = "https://csfloat.com/api/v1/listings"

headers = {
    "Authorization": api_key
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
