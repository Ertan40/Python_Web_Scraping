from bs4 import BeautifulSoup
import requests
import sqlite3


def fetch_data():
    url = "https://quotes.toscrape.com/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    raise Exception(f"failed to fetch data with error code: {response.status_code}")


def collect_data(html):
    soup = BeautifulSoup(html, "html.parser")
    quotes = soup.find_all("div", class_="quote")
    collection_dict = {}
    # collection_list = []
    if quotes:
        for quote in quotes:
            text = quote.find("span", class_="text").get_text(strip=True)
            author = quote.find("small", class_="author").get_text(strip=True)
            # data_collection.append({"author": author, "quote": text})
            if author not in collection_dict:
                collection_dict[author] = text
    return collection_dict


def save_data_to_db(collection_dict):
    connection = sqlite3.connect("quotes.db")
    cursor = connection.cursor()
    # create table
    cursor.execute('''
         CREATE TABLE quotes (
            id INTEGER PRIMARY KEY,
            Author TEXT, 
            Quote TEXT
         );
    ''')
    # insert data into the table
    for author, quote in collection_dict.items():
        cursor.execute('''
            INSERT INTO quotes (Author, Quote)
            VALUES (?, ?)
        ''', (author, quote))

    connection.commit()
    connection.close()


if __name__ == "__main__":
    data = fetch_data()
    main_data = collect_data(data)
    # print(main_data)
    # for author, quote in main_data.items():
    #     print(f"author: {author} - quote: {quote}")
    save_data_to_db(main_data)