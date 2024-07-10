# Task: 7. Write a Python program to extract and display all the header tags from en.wikipedia.org/wiki/Main_Page.

import requests
from bs4 import BeautifulSoup


def fetch_data():
    url = "https://en.wikipedia.org/wiki/Main_Page"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text

    raise Exception(f"Something went wrong due to an error: {response.status_code}")


def collect_data(html):
    soup = BeautifulSoup(html, "html.parser")
    all_header_titles = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    return all_header_titles


if __name__ == "__main__":
    data = fetch_data()
    main_data = collect_data(data)
    print(*main_data, sep="\n\n")