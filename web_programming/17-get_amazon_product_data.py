"""
This file provides a function which will take a product name as input from the user,
and fetch from Amazon information about products of this name or category.  The product
information will include title, URL, price, ratings, and the discount if available.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


def fetch_data(product):
    url = f'https://www.amazon.com/laptop/s?k={product}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.amazon.in/',
        'Connection': 'keep-alive'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as error:
        raise Exception(f"Not able to fetch data due to an error: {str(error)}")


def get_product_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', attrs={"class": "s-result-item", "data-component-type": "s-search-result"})
    # return items
    product_list = []
    for item in items:
        # Extract product title, URL, price, ratings and discount
        title_element = item.find('span', class_='a-size-medium')
        product_title = title_element.text.strip() if title_element else 'N/A'

        url_element = item.find('a', class_='a-link-normal', href=True)
        product_url = f"https://www.amazon.com{url_element['href']}" if url_element else 'N/A'

        price_whole = item.find('span', class_='a-price-whole')
        price_fraction = item.find('span', class_='a-price-fraction')
        price = f"${price_whole.text}{price_fraction.text}" if price_whole and price_fraction else 'N/A'

        rating_element = item.find('span', class_='a-icon-alt')
        rating = rating_element.text.strip() if rating_element else 'N/A'

        discount_element = item.find('span', class_='a-letter-space')
        discount = discount_element.text.strip() if discount_element else 'N/A'

        product_list.append({
            'Product title': product_title,
            'Product URL': product_url,
            'Product price': price,
            'Product rating': rating,
            'Product discount': discount
        })
    return product_list


# Usage
if __name__ == "__main__":
    product_input = input(f"Please enter the product you want to retrieve information: ")
    data = fetch_data(product_input)
    # print(get_product_data(data))
    products_data = get_product_data(data)
    df = pd.DataFrame(products_data)
    print(df)

    # Save to CSV file
    df.to_csv(f"{product_input}_products.csv", index=False)