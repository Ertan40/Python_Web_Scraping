import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_wikipedia_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        return response.text
    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {str(error)}")
        return None


def get_wikipedia_data(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="wikitable sortable sticky-header")
    if table:
        rows = table.find_all('tr')  # find all rows in the table
        return rows
    else:
        print("Table not found!")
        return []


def process_wikipedia_data(rows):
    # Extract headers from the first row and skip Rank
    headers = [header.get_text(strip=True) for header in rows[0].find_all('th')][1:]
    # Process the table rows
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        if cols:
            row_data = [col.get_text(strip=True) for col in cols]
            # Pad or truncate row data to match the number of headers
            if len(row_data) < len(headers):
                row_data.extend([""] * (len(headers) - len(row_data)))  # Pad missing columns
            elif len(row_data) > len(headers):
                row_data = row_data[:len(headers)]  # Truncate extra columns
            data.append(row_data)

    return headers, data


def save_to_csv(headers, data, filename):
    # Create a DataFrame using extracted data: headers and data
    df = pd.DataFrame(data, columns=headers)
    df.to_csv(filename, index=False)
    print(f"Data has been saved successfully to {filename}")


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/List_of_association_football_stadiums_by_capacity"
    page = get_wikipedia_page(url=url)
    if page:
        table_rows = get_wikipedia_data(page)  # Parse the table
        table_headers, table_data = process_wikipedia_data(table_rows)
        # Save the data to a CSV file
        save_to_csv(table_headers, table_data, "stadiums.csv")
        # Let's preview the extracted data
        print("Headers", table_headers)
        print("First row of data:", table_data[1])