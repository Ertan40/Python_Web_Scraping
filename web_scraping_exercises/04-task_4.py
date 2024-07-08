# Task: 4. Write a Python program to convert an address (like "1600 Amphitheatre Parkway, Mountain View,
# CA") into geographic coordinates (like latitude 37.423021 and longitude -122.083739). Geocodin: Geocoding is the
# process of converting addresses (like "1600 Amphitheatre Parkway, Mountain View, CA") into geographic coordinates (
# like latitude 37.423021 and longitude -122.083739), which you can use to place markers on a map, or position the map.
import requests

geo_url = 'https://maps.googleapis.com/maps/api/geocode/json'
my_address = {'address': 'Todor Djebarov street, Sofia, Bulgaira',
              'language': 'en'}

# Add your API key  - in order to have this code works as expected, you have to add valid API key
# my_address = {'address': 'Todor Djebarov street, Sofia, Bulgaira',
#               'language': 'en',
#               'key': 'YOUR_API_KEY_HERE'  # Replace with your actual API key
#                }

response = requests.get(geo_url, params=my_address)

# Check if the request was successful
if response.status_code == 200:
    results = response.json()

    # Print the entire response for debugging
    print("Full API Response:")
    print(results)

    if results['status'] == 'OK':
        if results['results']:
            my_geo = results['results'][0]['geometry']['location']
            print("Longitude:", my_geo['lng'], "\nLatitude:", my_geo['lat'])
        else:
            print("No results found for the given address.")
    else:
        print(f"API returned status: {results['status']}")
        if 'error_message' in results:
            print(f"Error message: {results['error_message']}")
else:
    print(f"Request failed with status code: {response.status_code}")