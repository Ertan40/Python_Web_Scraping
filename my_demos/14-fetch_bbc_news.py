import requests


params = {
    'apiKey': "Your API key goes here",
    'source': 'bbc-news',
    'sortBy': 'top'
}
BASE_URL = f"https://newsapi.org/v1/articles"


def fetch_bbc_news():
    try:
        response = requests.get(BASE_URL,params=params, timeout=10)
        response.raise_for_status()   # Raise HTTP errors if status code != 200
        return response.json()

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch data due to an error: {str(e)} ")


# Usage
if __name__ == '__main__':
    data = fetch_bbc_news()
    if data['status'] == 'ok':
        for d in data['articles']:
            print(f"Author: {d['author']}")
            print(f"Title: {d['title']}")
            print(f"Description: {d['description']}")
            print(f"For more info, please click at the following url: {d['url']}")
            print()
    else:
        raise Exception("Something went wrong!")

    # {'status': 'ok', 'source': 'bbc-news', 'sortBy': 'top',
    #  'articles': [{'author': 'BBC News', 'title': 'Dozens missing as'....}]}