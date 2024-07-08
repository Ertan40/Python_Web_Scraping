# Task: 3. Write a Python program to get the number of datasets currently listed on data.gov.

import requests
from bs4 import BeautifulSoup


def fetch_data():
    url = "https://data.gov/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    raise Exception(f"Not able to fetch data sue to error code: {response.status_code}")


def collect_data(html):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", class_="hero__dataset-count")
    if div:
        span = div.find("span", class_="text-color-red")
        return f"The number of datasets currently on data.gov: {span.text}"


if __name__ == "__main__":
    data = fetch_data()
    main_data = collect_data(data)
    print(main_data)
    # print(data)

# Shorter second version is below:
#
# from lxml import html
# import requests
#
# response = requests.get('http://www.data.gov/')
# doc_gov = html.fromstring(response.text)
#
# # In order to be used: pip install cssselect
# link_gov = doc_gov.cssselect('.text-color-red')
# print("Number of datasets currently listed on data.gov:")
#
# if link_gov:
#     # Access the first element's text content
#     print(link_gov[0].text_content().strip())
# else:
#     print("No element with class 'text-color-red' found")
