import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'
}


def fetch_data(symbol):
    try:
        BASE_URL = f"https://finance.yahoo.com/quote/{symbol}/"
        response = requests.get(BASE_URL, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses (4XX, 5XX)
        return response.text

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch data due to an error: {str(e)}")


# Get the current stock price and close time
def get_stock_price(html):
    soup = BeautifulSoup(html, 'html.parser')
    price_and_close_data = soup.find('div', class_='container yf-aay0dk')
    if price_and_close_data:
        text = price_and_close_data.text.split("EDT")
        at_close = text[0].split('At')
        price = at_close[0].strip()
        close = at_close[1].strip()

        return price, close
        # 187.99 -3.17 (-1.66%) At close: September 27 at 4:00 PM EDT    187.56 -0.41 (-0.22%) Pre-Market: 5:43 AM EDT
    else:
        raise Exception("Stock price information not found!")


# Usage - symbols: "AAPL AMZN IBM GOOG MSFT ORCL" search for symbols at https://finance.yahoo.com/
if __name__ == "__main__":
    # Available stock symbols
    abbreviations = ["AAPL", "AMZN", "IBM", "GOOG", "MSFT", "ORCL"]
    print(f"Available stock symbols: {', '.join(abbreviations)}")
    # Get input from user
    symbol_input = input("Please type one of the stock abbreviations from above: ").upper().strip()
    if symbol_input not in abbreviations:
        print("Invalid symbol. Please try again with a valid stock abbreviation.")
    else:
        try:
            # Fetch and parse the stock data
            data = fetch_data(symbol_input)
            # current_price = get_stock_price(data)[0]
            # current_at_close = get_stock_price(data)[1]
            current_price, current_at_close = get_stock_price(data)
            # Print the results
            print(f"Current {symbol_input} stock price is {current_price}")
            print(f"At {current_at_close} EDT")
        except Exception as e:
            print(f"Error occurred: {str(e)}")


# Output:
# Available stock symbols: AAPL, AMZN, IBM, GOOG, MSFT, ORCL
# Please type one of the stock abbreviations from above: IBM
# Current IBM stock price is 220.84 -2.59 (-1.16%)
# At close: September 27 at 4:00 PM EDT