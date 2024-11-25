from bs4 import BeautifulSoup
import os
import csv
import requests


def fetch_data():
    URL = 'https://en.wikipedia.org/wiki/List_of_European_Union_member_states_by_population'
    response = requests.get(URL)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Failed to fetch URL")


def extract_the_data(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('table', class_='wikitable')
    if table:
        rows = table.find_all("tr")[1:]  # Skip the header row
        return rows
    else:
        raise Exception('Table not found!')


def create_country_dictionary(rows):
    country_dict = {}
    for row in rows:
        columns = row.find_all('td')
        if len(columns) < 4:
            continue  # Skip rows that don't have the expected number of columns
        country = columns[0].text.strip()
        official_figure_str = columns[3].text.strip().replace(',', '')
        try:
            official_figure = int(official_figure_str)
        except ValueError:
            official_figure = None  # or any default value you want to use for invalid data

        if country not in country_dict:
            country_dict[country] = {'country_population': official_figure}
    return country_dict
# output - {'Germany': {'country_population': 84607016}, 'France': {'country_population': 67874000}....}


def calculate_total_population(country_dict):
    # total_population = 0
    country_dict_percentage = {}
    total_population = sum([entry['country_population'] for entry in country_dict.values()])
    # for country_info in country_dict.values():
    #     population = country_info.get('country_population')
    #     if population is not None:
    #         total_population += population
    for country, country_population in country_dict.items():  # ('Germany', {'country_population': 84607016})
        population = country_population.get("country_population")
        if population is not None:
            population_percentage = (population / total_population) * 100
            country_dict_percentage[country] = {
                "country_population": country_population["country_population"],
                "country_population_percentage": round(population_percentage, 1)
            }

    return country_dict_percentage
# {'Germany': {'country_population': 84607016


def copy_country_info_into_csv_file(country_dict):
    try:
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        file_path = os.path.join(desktop_path, 'List_of_European_Union_member.csv')
        with open(file_path, "w", newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Writing the header
            csv_writer.writerow(["Country", "Population", "Population Percentage"])
            for country, data in country_dict.items():
                csv_writer.writerow([country, data['country_population'], data['country_population_percentage']])
        return 'File is updated'
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    data = fetch_data()
    table = extract_the_data(data)
    country_data = create_country_dictionary(table)
    country_data_with_percentage = calculate_total_population(country_data)
    print(country_data_with_percentage)
    # result = copy_country_info_into_csv_file(country_data_with_percentage)
    # print(result)


