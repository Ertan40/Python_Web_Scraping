import requests


def fetch_joke_data():
    url = 'https://v2.jokeapi.dev/joke/Any'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Not able to fetch data due to the error: {response.status_code}")


def display_joke(current_data):
    if current_data['type'] == 'twopart':
        joke_info = {
            'category': current_data['category'],
            'type': current_data['type'],
            'setup': current_data['setup'],
            'delivery': current_data['delivery'],
        }
        return joke_info

    elif current_data['type'] == 'single':
        joke_info = {
            'category': current_data['category'],
            'type': current_data['type'],
            'joke': current_data['joke'],
        }
        return joke_info


if __name__ == '__main__':
    data = fetch_joke_data()
    joke = display_joke(data)
    if joke['type'] == 'single':
        print(f"Type: {joke['type']}\nJoke of the day: {joke['joke']}")
    else:
        print(f"Type: {joke['type']}\nQuestion: {joke['setup']}\nAnswer: {joke['delivery']}")




# Output:
#
# Type: twopart
# Question: What's the difference between a school bus and a cactus?
# Answer: A cactus keeps the little pricks on the outside.