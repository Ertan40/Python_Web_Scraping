import requests
from bs4 import BeautifulSoup

"""
Scraping jobs by entering a keyword on the Indeed website.
"""


def fetch_data(key_word):
    url = f'https://www.zaplata.bg/search?go=&keyword%5B0%5D={key_word}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch data due to an error: {str(e)}")


def process_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    job_items = soup.find_all('item')
    if not job_items:
        print("Няма намерени обяви с това търсене.")
    # return job_items
    current_jobs = []
    for item in job_items:
        title_div = item.find('div', class_='title')
        salary_div = item.find('div', class_='salary')
        city_div = item.find('div', class_='city')

        # Extract and clean text from each section if available
        title = title_div.text.strip() if title_div else 'No title available'
        salary = salary_div.text.strip() if salary_div else 'No salary information'
        city = city_div.text.strip() if city_div else 'No city information'

        # Store the job details in a dictionary and then append
        current_jobs.append({
            'title': title,
            'salary': salary,
            'city': city
        })

    return current_jobs


# Usage
if __name__ == "__main__":
    key_word_input = input(f"Please enter the key word: ").lower().strip()
    data = fetch_data(key_word_input)
    jobs = process_data(data)

    # print(jobs)
    if jobs:
        print(f"Обяви за Работа за {key_word_input}:")
    for job in jobs:
        print(f"Title: {job['title']}")
        print(f"Salary: {job['salary']}")
        print(f"City: {job['city']}")
        print('-' * 30)


# Output:
# Please enter the key word: devops
# Обяви за Работа за devops:
# Title: Full-Stack PHP Developer
# Salary: от  4900  до  6600 лв. бруто
# City: гр.София / 30 Септември
# ------------------------------
# Title: Senior Backend Software Engineer
# Salary: от  7500  до  9000 лв. бруто
# City: гр.София / 30 Септември
# ------------------------------
# Title: System and Security Administrator (Linux/Windows)
# Salary: от  5000  до  10000 лв. бруто
# City: гр.София / 25 Септември
# ------------------------------
# Title: DevOps Engineer
# Salary: от  5500  до  6000 лв. бруто
# City: гр.София / 25 Септември
# ------------------------------