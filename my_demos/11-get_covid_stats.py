from bs4 import BeautifulSoup
import requests


url = "https://www.worldometers.info/coronavirus/"


def fetch_data():
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.text
    raise Exception(f"Failed to get data due ti an error code: {response.status_code}")


def retrieve_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    main_div = soup.find_all('div', class_='maincounter-number')
    covid_cases = []
    if main_div:
        for div in main_div:
            span = div.find('span')
            if span:
                case = span.text.strip()
                covid_cases.append(case)
            else:
                raise Exception("Span not found!")
        return covid_cases
    else:
        raise Exception("Main div not found!")


# Test case
if __name__ == "__main__":
    data = fetch_data()
    cases = retrieve_data(data)
    # print(retrieve_data(data))
    print(f"Total COVID-19 cases in the world: {cases[0]}")
    print(f"Total deaths due to COVID-19 in the world: {cases[1]}")
    print(f"Total COVID-19 patients recovered in the world {cases[2]}")