import os.path
import shutil

import requests

url = 'https://api.nasa.gov/planetary/apod'
params = {'api_key': 'your_api_key'}
"""
Get the APOD(Astronomical Picture of the day) data
Get your API Key from: https://api.nasa.gov/
"""


def fetch_data():
    try:
        response = requests.get(url, params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Failed to fetch data due to an error: {str(error)}")
        return None


# Save the APOD image to the local system
def save_apod(apod_data):
    media_type = apod_data.get('media_type')
    if media_type != 'image':
        print("Media type is not an image, skipping download")
        return
    image_url = apod_data.get('url')
    image_name = apod_data.get('title')
    # image_name = "".join([c if c.isalnum() or c in (' ', '_') else '_' for c in apod_data.get('title')])
    save_path = 'C:\\Users\\ertan\\downloads'

    # Extract the image file extension from the URL - jpeg or png
    ext = os.path.splitext(image_url)[1]
    full_path = os.path.join(save_path, f"{image_name}{ext}")

    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        with open(full_path, 'wb') as image_file:
            shutil.copyfileobj(response.raw, image_file)
        print(f"Image {image_name} saved successfully to {full_path}")

    except requests.exceptions.RequestException as error:
        print(f"Failed to download the image due to an error: {str(error)}")


# Usage
if __name__ == "__main__":
    data = fetch_data()
    if data:
        # print(data)
        print(f"Title: {data.get('title')}")
        print(f"Copyright: {data.get('copyright')}")
        print(f"Date: {data.get('date')}")
        print(f"Explanation: {data.get('explanation')}")
        print(f"Media type: {data.get('media_type')}")
        print(f"Service version: {data.get('service_version')}")
        if url:
            print(f"URL of the image: {data.get('url')}")
            save_apod(data)
        else:
            print("URL of the image: Unfortunately there is no URL for this image")

# Output:
# Title: NGC 7293: The Helix Nebula
# Copyright: Patrick Winkler
# Date: 2024-10-24
# Explanation: A mere seven hundred light years from Earth toward the constellation Aquarius, a star is dying...
# Media type: image
# Service version: v1
# URL of the image: https://apod.nasa.gov/apod/image/2410/NGC7293_preview1024.png
# Image NGC 7293: The Helix Nebula saved successfully to C:\Users\ertan\downloads\NGC 7293: The Helix Nebula.png