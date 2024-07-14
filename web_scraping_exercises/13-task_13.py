# Task: Write a Python program to get the number of people visiting a U.S. government website right now.
# Source: https://analytics.usa.gov/data/live/realtime.json


import json
import requests


url = "https://analytics.usa.gov/data/live/realtime.json"
response = requests.get(url)
if response.status_code == 200:
    data = response.json()  # parse the response content as JSON
    # print(json.dumps(data, indent=4))    # to print the JSON data in a readable format with indentation.
    active_visitors = data["data"][0]["active_visitors"]
    print("Number of people visiting a U.S. government website-")
    print(f"Active Users Right Now: {int(active_visitors)}")

else:
    print(f"Failed to fetch data due to error: {response.status_code}")