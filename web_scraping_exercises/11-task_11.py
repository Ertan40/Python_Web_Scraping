# Task: 11. Write a Python program to check whether a page contains a title or not. "https://www.w3resource.com/"


import requests
from bs4 import BeautifulSoup


def fetch_data():
    # url = "https://www.w3resource.com/"
    url = "https://www.example.com/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    raise Exception(f"failed to fetch due to error: {response.status_code}")


def get_titles(html):
    soup = BeautifulSoup(html, "html.parser")
    titles = soup.find_all("h1")
    return titles


if __name__ == "__main__":
    data = fetch_data()
    titles = get_titles(data)
    if titles:
        print("Titles found on the page:")
        for title in titles:
            print(title.get_text(strip=True))
    else:
        print("No titles found on the page.")

