import requests
from datetime import date


url = 'https://api.carbonintensity.org.uk/intensity'


def fetch_data():
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Failed to fetch data due to the error code: {response.status_code}")


# {'data': [{'from': '2024-09-24T11:30Z', 'to': '2024-09-24T12:00Z', 'intensity': {'forecast': 146, 'actual': 146,
# 'index': 'moderate'}}]}
def last_half_hour(current_data):
    intensity_data = current_data['data'][0]['intensity']
    return (f"Forecast: {intensity_data['forecast']}\nActual: {intensity_data['actual']}\n"
            f"Index: {intensity_data['index']}")


def fetch_from_to(start, end):
    start_str = start.strftime('%Y-%m-%d')
    end_str = end.strftime('%Y-%m-%d')
    response = requests.get(f"{url}/{start_str}/{end_str}", timeout=10)

    if response.status_code == 200:
        return response.json()['data']
    raise Exception(f"Failed to fetch data due to the error: {response.status_code}")


if __name__ == "__main__":
    # Fetch the last half-hour data
    data = fetch_data()
    print(last_half_hour(data))
    # Fetch the data between two dates
    start_date = date(2024, 9, 1)
    end_date = date(2024, 9, 2)
    print("---------------------o---------------------")
    for data_item in fetch_from_to(start_date, end_date):
        print(f"From {data_item['from']} to {data_item['to']}: {data_item['intensity']['actual']}")