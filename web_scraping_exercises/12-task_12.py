# Task: 12. Write a Python program to list all language names and number of related articles in the order
# they appear in wikipedia.org.

#
import requests
from bs4 import BeautifulSoup


def fetch_data():
    url = "https://www.wikipedia.org/"
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response.text
    raise Exception(f"failed to fetch due to error: {response.status_code}")


def get_languages(html):
    soup = BeautifulSoup(html, "html.parser")
    languages_section = soup.find_all("a", class_="link-box")
    # for language in language_section:
    #     print(language.get_text())
    if languages_section:
        languages = []
        for language in languages_section:
            lang_name = language.find("strong").get_text(strip=True)
            lang_count = language.find("small").get_text(strip=True)
            # If you'd like to remove the suffix starting from the '+'
            # if '+' in lang_count:
            #     lang_count = lang_count.split('+')[0].strip()
            languages.append((lang_name, lang_count))
        return languages
    else:
        print("Languages not found")
        return []


if __name__ == "__main__":
    data = fetch_data()
    languages = get_languages(data)
    if languages:
        print("Languages found on the page:")
        for lang_name, lang_count in languages:
            print(f"\n{lang_name}: {lang_count}")
    else:
        print("No languages found on the page.")



