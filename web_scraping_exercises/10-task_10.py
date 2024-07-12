# Task: 10. Write a Python program to that retrieves an arbitary Wikipedia page of
# "Python" and creates a list of links on that page.

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def fetch_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch due to error: {e}")


def collect_data(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for link in soup.find_all("a", href=True):
        full_url = urljoin(base_url, link['href'])
        if full_url.startswith(('http://', 'https://')):
            links.append(full_url)
    return links


def main():
    url = "https://en.wikipedia.org/wiki/Python"
    try:
        html_content = fetch_data(url)
        links = collect_data(html_content, url)
        print(f"Found {len(links)} links:")
        for link in links[:20]:  # Print first 20 links as an example
            print(link)
        print("...")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
