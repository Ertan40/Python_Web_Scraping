from bs4 import BeautifulSoup
import requests
import psycopg2


def fetch_data():
    url = "https://quotes.toscrape.com/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    raise Exception(f"Failed to fetch data with error code: {response.status_code}")


def collect_data(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes = soup.find_all("div", class_="quote")
    collection_dict = {}
    if quotes:
        for quote in quotes:
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            if author not in collection_dict:
                collection_dict[author] = text
    return collection_dict


def save_data_to_db(collection_dict):
    # Connect to PostgreSQL
    connection = psycopg2.connect(
        dbname="quotes_db",
        user="postgres-user",
        password="password",
        host="127.0.0.1",
        port="5432"
    )
    cursor = connection.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id SERIAL PRIMARY KEY,
            Author TEXT, 
            Quote TEXT
        );
    ''')

    # Insert data into the table
    for author, quote in collection_dict.items():
        cursor.execute('''
            INSERT INTO quotes (Author, Quote)
            VALUES (%s, %s)
        ''', (author, quote))

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    data = fetch_data()
    main_data = collect_data(data)
    save_data_to_db(main_data)
