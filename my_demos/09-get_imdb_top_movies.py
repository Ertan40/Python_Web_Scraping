import requests
from bs4 import BeautifulSoup


def imdb_top(imdb_top_n):
    base_url = f"https://www.imdb.com/search/title/?title_type=feature&count={imdb_top_n}&sort=num_votes,desc"
    headers = {
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                               'Chrome/91.0.4472.124 Safari/537.36'
             }
    response = requests.get(base_url, headers=headers, timeout=10)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the movie title containers
        movie_divs = soup.find_all('div', class_='ipc-title')

        # Extract movie titles from the content
        top_movies = []
        for movie in movie_divs:
            title_tag = movie.find('h3', class_='ipc-title__text')
            if title_tag:
                title = title_tag.text.strip()
                top_movies.append(title)

        if not top_movies:
            raise Exception("Could not find any titles. The HTML structure may have changed.")

        top_movies = top_movies[:-1]  # Remove 'recently viewed'

        return '\n'.join(top_movies)

    raise Exception(f"Error code: {response.status_code}")


# Example usage:
# print(imdb_top(6))
if __name__ == "__main__":
    print("Please enter the number of top movies you would like to get: ")
    user_input = int(input(f"Number of movies: "))
    if user_input < 1:
        raise ValueError("The number of movies should be a positive integer.")

    print(f"Top {user_input} Movies from IMDb")
    print(imdb_top(user_input))

# Output:
# Please enter the number of top movies you would like to get:
# Number of movies: 5
# Top 5 Movies from IMDb
# 1. The Shawshank Redemption
# 2. The Dark Knight
# 3. Inception
# 4. Fight Club
# 5. Forrest Gump