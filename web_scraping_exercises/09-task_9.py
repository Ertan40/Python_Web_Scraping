# Task: 9. Write a Python program to get 30 days of visits broken down by browser for all sites on data.gov.


import requests


def fetch_data():
    url = "https://analytics.usa.gov/data/live/browsers.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"failed to fetch due to error: {response.status_code}")


def format_number(num):
    return f"{num:,}"


if __name__ == "__main__":
    data = fetch_data()
    print("30 days of visits broken down by browser for all sites:")

    if 'totals' in data and 'by_browser' in data['totals']:
        browser_data = data['totals']['by_browser']
        for browser, visits in browser_data.items():
            print(f"{browser}: {format_number(visits)}")
    else:
        print("No browser data found in the response.")



