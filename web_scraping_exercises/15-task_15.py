# Task: Write a Python program to download IMDB's Top 250 data (movie name, Initial release, director name and writers).
## Please note that web scraping can be fragile, and if IMDb significantly changes their page structure,
# this code might need to be updated again.

import requests
from bs4 import BeautifulSoup
import time


def fetch_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    raise Exception(f"Not able to fetch data due to an error: {response.status_code}")


def collect_data(html):
    soup = BeautifulSoup(html, "html.parser")
    movie_items = soup.find_all("li", class_="ipc-metadata-list-summary-item")

    all_data = []
    for index, item in enumerate(movie_items, start=1):
        title_elem = item.find("h3", class_="ipc-title__text")
        title = title_elem.text.split('. ', 1)[1] if title_elem else "N/A"

        year_elem = item.find("span", class_="cli-title-metadata-item")
        year = year_elem.text if year_elem else "N/A"

        movie_link = "https://www.imdb.com" + item.find("a")['href']
        director, writers = get_movie_details(movie_link)

        movie_info = f"{index} - {title} ({year}) - Starring: {director} (dir.), {writers}"
        all_data.append(movie_info)
        print(movie_info)  # Print as we go

        time.sleep(1)  # In order to not overload the server
        if index == 10:  # Just first 10 to display
            break
    return all_data


def get_movie_details(url):
    html = fetch_data(url)
    soup = BeautifulSoup(html, "html.parser")

    director_elem = soup.find("a", class_="ipc-metadata-list-item__list-content-item--link",
                              attrs={"href": lambda x: x and x.startswith("/name/")})
    director = director_elem.text if director_elem else "N/A"

    writer_elems = soup.find_all("a", class_="ipc-metadata-list-item__list-content-item--link",
                                 attrs={"href": lambda x: x and x.startswith("/name/")})
    writers = ", ".join([writer.text for writer in writer_elems[1:3]]) if len(writer_elems) > 1 else "N/A"

    return director, writers


if __name__ == "__main__":
    main_url = "https://www.imdb.com/chart/top/"
    data = fetch_data(main_url)
    all_data = collect_data(data)



## You can find below expected output below for first 10:
# 1 - The Shawshank Redemption (1994) - Starring: Frank Darabont (dir.), Stephen King, Frank Darabont
# 2 - The Godfather (1972) - Starring: Francis Ford Coppola (dir.), Mario Puzo, Francis Ford Coppola
# 3 - The Dark Knight (2008) - Starring: Christopher Nolan (dir.), Jonathan Nolan, Christopher Nolan
# 4 - The Godfather Part II (1974) - Starring: Francis Ford Coppola (dir.), Francis Ford Coppola, Mario Puzo
# 5 - 12 Angry Men (1957) - Starring: Sidney Lumet (dir.), Reginald Rose, Henry Fonda
# 6 - Schindler's List (1993) - Starring: Steven Spielberg (dir.), Thomas Keneally, Steven Zaillian
# 7 - The Lord of the Rings: The Return of the King (2003) - Starring: Peter Jackson (dir.), J.R.R. Tolkien, Fran Walsh
# 8 - Pulp Fiction (1994) - Starring: Quentin Tarantino (dir.), Quentin Tarantino, Roger Avary
# 9 - The Lord of the Rings: The Fellowship of the Ring (2001) - Starring: Peter Jackson (dir.), J.R.R. Tolkien, Fran Walsh
# 10 - Il buono, il brutto, il cattivo (1966) - Starring: Sergio Leone (dir.), Luciano Vincenzoni, Sergio Leone
