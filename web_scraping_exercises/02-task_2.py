#  Task: 2. Write a Python program to download and display the content of robot.txt for en.wikipedia.org.

import requests


def fetch_data():
    url = "https://en.wikipedia.org/wiki/Robots.txt"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    raise Exception(f"Not able to fetch data sue to error code: {response.status_code}")


if __name__ == "__main__":
    data = fetch_data()
    print("robots.txt for http://www.wikipedia.org/")
    print("===================================================")
    print(data)