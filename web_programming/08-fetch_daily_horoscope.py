from bs4 import BeautifulSoup
import requests


def fetch_horoscope(zodiac_sign, day):
    url = f'https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-{day}.aspx?sign={zodiac_sign}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        horoscope_p = soup.find('div', class_='main-horoscope').find('p')
        if horoscope_p:
            horoscope_text = horoscope_p.text.strip()
            return horoscope_text
        else:
            raise Exception("Could not find the horoscope section. The HTML structure may have changed.")
    else:
        raise Exception(f"Failed to fetch data due to the error code: {response.status_code}")


def get_valid_input(prompt, options):
    """Helper function to repeatedly prompt user for valid input."""
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in options:
            return user_input
        print(f"Invalid input! Please choose from {', '.join(options)}.")


if __name__ == '__main__':
    print("Your Horoscope\n")
    print("Please choose your Zodiac sign number from below:\n",
          "1. Aries\n",
          "2. Taurus\n",
          "3. Gemini\n",
          "4. Cancer\n",
          "5. Leo\n",
          "6. Virgo\n",
          "7. Libra\n",
          "8. Scorpio\n",
          "9. Sagittarius\n",
          "10. Capricorn\n",
          "11. Aquarius\n",
          "12. Pisces\n", )

    allowed_signs = [str(s) for s in range(1, 13)]
    requested_sign = get_valid_input("Please enter your Zodiac sign number: ", allowed_signs)

    print("Please choose a day from the following options: today, yesterday, or tomorrow.")
    allowed_days = ['today', 'yesterday', 'tomorrow']
    requested_day = get_valid_input("Enter the day: ", allowed_days)

    try:
        result = fetch_horoscope(requested_sign, requested_day)
        # print(result)  # or in one line
        # I printed it this way because I like how it looks, rather than printing it on one line.
        formated_text = result.split('. ')
        joined_text = '.\n'.join(formated_text).strip()
        print(joined_text)
    except Exception as e:
        print(f"Error: {e}")

# Output:
# Sep 18, 2024 - Today is a fantastic day, Pisces, so make the most of it.
# If you're emotionally and mentally prepared to go on a new, exciting life journey, the opportunity will present itself.
# The energy will be fast and furious.
# You can work harmoniously with electrical gadgets and new technologies.
# Break free of the mundane and seek less conventional ways of living.
