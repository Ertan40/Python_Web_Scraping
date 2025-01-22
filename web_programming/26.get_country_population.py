import requests
from bs4 import BeautifulSoup


def extract_table_data():
    url = 'https://en.wikipedia.org/wiki/List_of_European_Union_member_states_by_population'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find('table', class_='wikitable')
        table_rows = table.find_all('tr')
        return table_rows

    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {str(error)}")
        return None


def transform_table_data(rows_data):
    countries_dictionary = {}

    for i in range(1, len(rows_data) - 1):
        tds = rows_data[i].find_all('td')
        country = tds[0].text.strip()
        population = int(tds[1].text.replace(',', '').strip())

        countries_dictionary[country] = {'country_population': population}

    return countries_dictionary
# Output:
# {'Germany': {'country_population': 83445000}, 'France': {'country_population': 68402000},
#  'Italy': {'country_population': 58989700},...


def calculate_total_population_data(countries_dictionary):
    total_population = sum(c['country_population'] for c in countries_dictionary.values())

    for country, population in countries_dictionary.items():
        calculate_percentage = (population['country_population'] / total_population) * 100
        countries_dictionary[country]['country_population_percentage'] = round(calculate_percentage, 1)

    return countries_dictionary


if __name__ == "__main__":
    fetched_data = extract_table_data()
    # print(fetched_data)
    data_table_rows = transform_table_data(fetched_data)
    # print(data_table_rows)
    countries_population = calculate_total_population_data(data_table_rows)
    for country, population in countries_population.items():
        print(f"{country}: {population}")


#Output:
# Germany: {'country_population': 83445000, 'country_population_percentage': 18.6}
# France: {'country_population': 68402000, 'country_population_percentage': 15.2}
# Italy: {'country_population': 58989700, 'country_population_percentage': 13.1}
# Spain: {'country_population': 48610500, 'country_population_percentage': 10.8}
# Poland: {'country_population': 36621000, 'country_population_percentage': 8.2}
# Romania: {'country_population': 19064400, 'country_population_percentage': 4.2}
# Netherlands: {'country_population': 17942900, 'country_population_percentage': 4.0}
# Belgium: {'country_population': 11832000, 'country_population_percentage': 2.6}
# Czech Republic: {'country_population': 10900600, 'country_population_percentage': 2.4}
# Portugal: {'country_population': 10639700, 'country_population_percentage': 2.4}
# Sweden: {'country_population': 10551700, 'country_population_percentage': 2.3}
# Greece: {'country_population': 10397200, 'country_population_percentage': 2.3}
# Hungary: {'country_population': 9584600, 'country_population_percentage': 2.1}
# Austria: {'country_population': 9158800, 'country_population_percentage': 2.0}
# Bulgaria: {'country_population': 6445500, 'country_population_percentage': 1.4}
# Denmark: {'country_population': 5961200, 'country_population_percentage': 1.3}
# Finland: {'country_population': 5603900, 'country_population_percentage': 1.2}
# Slovakia: {'country_population': 5424700, 'country_population_percentage': 1.2}
# Ireland: {'country_population': 5343800, 'country_population_percentage': 1.2}
# Croatia: {'country_population': 3862000, 'country_population_percentage': 0.9}
# Lithuania: {'country_population': 2885900, 'country_population_percentage': 0.6}
# Slovenia: {'country_population': 2123900, 'country_population_percentage': 0.5}
# Latvia: {'country_population': 1871900, 'country_population_percentage': 0.4}
# Estonia: {'country_population': 1374700, 'country_population_percentage': 0.3}
# Cyprus: {'country_population': 933500, 'country_population_percentage': 0.2}
# Luxembourg: {'country_population': 672100, 'country_population_percentage': 0.1}
# Malta: {'country_population': 563000, 'country_population_percentage': 0.1}