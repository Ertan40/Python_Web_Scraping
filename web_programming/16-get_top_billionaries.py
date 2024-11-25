from datetime import datetime
import requests


def fetch_data(limit):
    api_url = (
        f"https://www.forbes.com/forbesapi/person/rtb/0/position/true.json?fields=personName,gender,source,"
        f"countryOfCitizenship,birthDate,finalWorth&limit={limit}"
    )
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        return response.json()
    # {'personList': {'personsLists': [{'finalWorth': 263958.372, 'personName': 'Elon Musk', 'source': 'Tesla,
    # SpaceX', 'countryOfCitizenship': 'United States', 'gender': 'M', 'birthDate': 46915200000, 'wealthList': False,
    # 'familyList': False, 'bioSuppress': False},......
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch data due to an error: {str(e)}")


def display_data(person_data):
    if person_data and 'personList' in person_data and person_data['personList'].get('personsLists'):
        for person in person_data['personList']['personsLists']:
            print(f"Person Name: {person['personName']}")
            print(f"Worth ($): {person['finalWorth'] / 1000:.2f} Billion")
            print(f"Source of Wealth: {person['source']}")
            print(f"Country of Citizenship: {person['countryOfCitizenship']}")
            print(f"Gender: {person['gender']}")
            # Check if 'birthDate' exists and is a valid timestamp
            if 'birthDate' in person and isinstance(person['birthDate'], (int, float)):
                try:
                    # Format birthdate from timestamp
                    birth_date = datetime.utcfromtimestamp(person['birthDate'] / 1000).strftime('%Y-%m-%d')
                    print(f"Birth Date: {birth_date}")
                except (OSError, ValueError) as e:
                    # Handle invalid timestamp
                    print(f"Birth Date: Invalid timestamp ({person['birthDate']})")
            else:
                print(f"Birth Date: N/A")
            print('-' * 40)
    else:
        print("No data found or invalid data structure.")


# Usage
if __name__ == "__main__":
    try:
        api_limit = int(input("Please enter the number of billionaires you want to display: "))
        data = fetch_data(api_limit)
        display_data(data)
    except ValueError:
        print("Please enter a valid number.")
    except Exception as e:
        print(str(e))