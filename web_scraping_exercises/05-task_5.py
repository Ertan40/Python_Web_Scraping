# Task: 5. Write a Python program to display the name of the most recently added dataset on data.gov.

import requests
from bs4 import BeautifulSoup


def fetch_data():
    url = "https://catalog.data.gov/dataset?q=&sort=metadata_created+desc"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text

    raise Exception(f"Not able to fetch data sue to error code: {response.status_code}")


def collect_data(html):
    soup = BeautifulSoup(html, "html.parser")
    dataset_items = soup.find_all("h3", class_="dataset-heading")
    if dataset_items:
        return dataset_items[0].text.strip()
    return "No datasets found"


if __name__ == "__main__":
    data = fetch_data()
    main_data = collect_data(data)
    print("The name of the most recently added dataset on data.gov:")
    print(main_data)


# Shorter second way is below:

# from lxml import html
# import requests
# response = requests.get('http://catalog.data.gov/dataset?q=&sort=metadata_created+desc')
# doc = html.fromstring(response.text)
# title = doc.cssselect('h3.dataset-heading')[0].text_content()
# print("The name of the most recently added dataset on data.gov:")
# print(title.strip())