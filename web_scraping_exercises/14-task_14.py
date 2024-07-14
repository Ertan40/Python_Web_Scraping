# Task: 14. Write a Python program to find the live weather report (temperature, wind speed, description and weather)
# of a given city.

# Please note that you have to register and get your own API!

import requests


def weather_data(query):
    res = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?' + query + '&APPID=6ba7c195793ee90a2c1be5134987e7bf&units=metric')
    res.raise_for_status()
    return res.json()


def print_weather(result, city):
    print("{}'s temperature: {}°C ".format(city, result['main']['temp']))
    print("Wind speed: {} m/s".format(result['wind']['speed']))
    print("Description: {}".format(result['weather'][0]['description']))
    print("Weather: {}".format(result['weather'][0]['main']))


def main():
    city = input('Enter the city: ')
    print()
    try:
        query = 'q=' + city
        w_data = weather_data(query)
        print_weather(w_data, city)
        print()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occurred: {req_err}')
    except KeyError as key_err:
        print(
            f'Key error occurred: {key_err}. The city might not be found or the API response format might have changed.')
    except Exception as err:
        print(f'An unexpected error occurred: {err}')


if __name__ == '__main__':
    main()

## Output:
# Enter the city: London,GB
#
# London,GB's temperature: 16.85°C
# Wind speed: 3.09 m/s
# Description: overcast clouds
# Weather: Clouds
