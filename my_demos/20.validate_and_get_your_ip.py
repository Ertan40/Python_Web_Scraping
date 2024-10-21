"""
New version: I have added validate_ip function with regex
"""

import requests
import re


def validate_ip(ip):
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ip_pattern, ip):
        return True
    else:
        print("Invalid IP format. Please enter a valid IP address.")
        return False


def fetch_data(ip):
    url = f'http://ip-api.com/json/{ip}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['status'] == 'fail':
            print(f"Error: {data['message']}")
            return None
        return data

    except requests.exceptions.RequestException as error:
        print(f"Network error occurred: {error}")
        return None


def display_ip_details(information):
    print(f"IP: {information['query']}")
    print(f"Country: {information['country']}")
    print(f"Country code: {information['countryCode']}")
    print(f"Region: {information['region']}")
    print(f"City: {information['city']}")
    print(f"ISP: {information['isp']}")
    print(f"Postal Code: {information['zip']}")
    print(f"Timezone: {information['timezone']}")


## Usage
if __name__ == '__main__':
    while True:
        input_ip = input("Please type the IP address you'd like to get information for ")
        if validate_ip(input_ip):
            data = fetch_data(input_ip)
            if data:
                display_ip_details(data)
            else:
                print("Failed to fetch data for the given IP")

        retry = input("\nWould you like to check another IP address? (y/n): ").strip().lower()
        if retry != 'y':
            print("Goodbye!")
            break