# Task: 1. Write a Python program to test if a given page is found or not on the server.

from urllib.request import urlopen
from urllib.error import HTTPError, URLError


def main():
    try:
        with urlopen("https://quotes.toscrape.com/") as response:
            html = response.read().decode('utf-8')  # The html.read() returns bytes. Therefore decode it to a string
            print("HTML details:")
            print(html)
        return 0
    except HTTPError as e:
        print(f"HTTP error occurred: {e.code} - {e.reason}")
    except URLError as e:
        print(f"Server not found: {e.reason}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return 1


if __name__ == "__main__":
    exit(main())
