import requests
import json


def fetch_data():
    url = 'https://randomuser.me/api/'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"Other error occurred: {err}")


data = fetch_data()

# Print the data in a formatted JSON structure for better readability
print(json.dumps(data, indent=4))