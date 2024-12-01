import requests
import certifi


def is_secure_website(url):
    try:
        response = requests.get(url, verify=certifi.where())
        response.raise_for_status()
        return response.url.startswith("https://")
    except requests.exceptions.RequestException as error:
        print(f"Error occurred: {str(error)}")
        return False


# Usage
if __name__ == "__main__":
    website_url = input(f"Please enter the website URL: ")
    if is_secure_website(website_url):
        print(f"\n{website_url} is a secure website.")
    else:
        print(f"\n{website_url} is not a secure website")