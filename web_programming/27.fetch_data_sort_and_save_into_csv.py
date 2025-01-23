import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
url = "https://bnb.bg/Statistics/StInterbankForexMarket/index.htm"


def fetch_data():
    """Fetches HTML content from the given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.exceptions.RequestException as error:
        print(f"An error occurred: {str(error)}")
        return None


def fetch_table_data(html):
    """Extracts table rows from HTML based on the given table class."""
    if not html:
        raise ValueError("No HTML content provided to extract data from.")

    soup = BeautifulSoup(html, 'html.parser')
    table_data = soup.find('table', class_='table')
    if not table_data:
        raise Exception("Table data not found!")

    trs = table_data.find_all('tr')

    return trs


def transform_data_rows(extracted_rows):
    """Transforms table rows into structured data."""
    data = []
    # for row in rows[1:]:
    #     tds = row.find_all('td')
    #     if len(tds) != 10:
    #         continue
    for i in range(2, len(extracted_rows) - 1):
        tds = extracted_rows[i].find_all('td')
        # data.append(tds)
        data_dict = {
            "Код на валута": tds[0].text.strip(),
            "no_value": tds[1].text.strip(),
            "купува": tds[2].text.strip(),
            "продава": tds[3].text.strip(),
            "купени_%": tds[4].text.strip(),
            "продадени_%": tds[5].text.strip(),
            "обем купени": tds[6].text.strip(),
            "обем продадени": tds[7].text.strip(),
            "купува_euro": tds[8].text.strip(),
            "продава_euro": tds[9].text.strip()
        }
        data.append(data_dict)

    return data


def turn_into_dataframe(transformed_data):
    """Converts structured data into a Pandas DataFrame."""
    return pd.DataFrame(transformed_data)


def sort_column_obem_prodadeni_in_descending_by_values(data_df):
    """Sorts the DataFrame by the 'обем продадени' column in descending order."""
    if 'обем продадени' not in data_df.columns:
        raise KeyError("Column 'обем продадени' not found in the DataFrame.")

    data_df['обем продадени'] = data_df['обем продадени'].str.replace(" ", "").astype(int)
    # Sort the DataFrame by 'обем продадени' in descending order
    sorted_df = data_df.sort_values(by='обем продадени', ascending=False)

    return sorted_df


def save_sorted_df_to_csv(sorted_data):
    """Saves the sorted DataFrame to a timestamped CSV file."""

    file_name = f"foreign_currency_against_leva_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    sorted_data.to_csv(file_name, index=False)
    return f"File written successfully to {file_name}!"


if __name__ == "__main__":
    html_content = fetch_data()
    if html_content:
        rows = fetch_table_data(html_content)
        data = transform_data_rows(rows)
        df = turn_into_dataframe(data)
        sorted_df = sort_column_obem_prodadeni_in_descending_by_values(df)
        save_sorted_df_to_csv(sorted_df)
        print(save_sorted_df_to_csv(sorted_df))