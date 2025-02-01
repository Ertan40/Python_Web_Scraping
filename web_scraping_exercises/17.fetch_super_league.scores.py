import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set the directory path to store the webpage
path = "C:\\Users\\ertan\\Downloads\\score_scraping"


def fetch_webpage():
    # Initialize WebDriver properly
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    url = 'https://www.flashscore.com.tr/futbol/turkiye/super-li-g/puan-durumu/#/jy5jZF2o/table/overall'

    driver.get(url)
    # Wait for the table to load dynamically
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ui-table__row'))
        )
    except Exception as e:
        print("Table did not load:", e)
        driver.quit()
        return None

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Ensure the directory exists
    os.makedirs(path, exist_ok=True)

    # Save the webpage to a file
    file_path = os.path.join(path, "score_page.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html)

    driver.quit()  # Close the browser properly

    return soup


def transform_data(soup):
    table = soup.find('div', class_='ui-table__body')
    if table:
        rows = table.find_all('div', class_='ui-table__row')
        football_teams = []
        if rows:
            for row in rows:
                # Extract team name first, because didn't work with 'table__cell'
                team_name = row.find('a', class_='tableCellParticipant__name')
                team_name = team_name.get_text(strip=True) if team_name else "N/A"

                # Extract other values (O, G, B, M, GI, AV, points)
                cells = row.find_all('span', class_='table__cell--value')
                if cells and len(cells) >= 7:  # Ensure there are enough cells
                    teams_info = {
                        'team': team_name,
                        'O': cells[0].get_text(strip=True),
                        'G': cells[1].get_text(strip=True),
                        'B': cells[2].get_text(strip=True),
                        'M': cells[3].get_text(strip=True),
                        'GI': cells[4].get_text(strip=True),
                        'AV': cells[5].get_text(strip=True),
                        'points': cells[6].get_text(strip=True)
                    }
                    football_teams.append(teams_info)
            return football_teams
        else:
            print("Rows not found!")
            return None
    else:
        print('Table not found!')
        return None


if __name__ == "__main__":
    soup = fetch_webpage()
    if soup:
        table_data = transform_data(soup)
        if table_data:
            df = pd.DataFrame(table_data)
            # Save to CSV file
            csv_path = os.path.join(path, 'football_points.csv')
            df.to_csv(csv_path, index=False)
            print(f"Table saved successfully in CSV file at: {csv_path}")
        else:
            print("No table data found.")
    else:
        print("Failed to fetch webpage.")


# Output + from csv file:
# Table saved successfully in CSV file at: C:\Users\ertan\Downloads\score_scraping\football_points.csv
# team	O	G	B	M	GI	AV	points
# Galatasaray	20	17	3	0	53:22	31	54
# Fenerbahçe	20	15	3	2	52:20	32	48
# Samsunspor	20	12	4	4	34:19	15	40
# Eyüpspor	21	11	6	4	34:19	15	39
# Göztepe	20	10	4	6	40:26	14	34
# Beşiktaş	20	8	8	4	29:21	8	32
# Başakşehir	20	8	5	7	35:30	5	29
# Rizespor	20	8	3	9	22:31	-9	27
# Gaziantep FK	20	7	5	8	26:28	-2	26
# Trabzonspor	19	6	7	6	34:24	10	25
# Alanyaspor	20	6	7	7	24:28	-4	25
# Kasımpaşa	20	5	10	5	32:37	-5	25
# Antalyaspor	21	7	4	10	25:41	-16	25
# Konyaspor	21	6	6	9	27:33	-6	24
# Sivasspor	21	6	5	10	26:35	-9	23
# Bodrumspor	21	4	4	13	15:29	-14	16
# Kayserispor	19	3	7	9	19:39	-20	16
# Hatayspor	21	1	7	13	23:40	-17	10
# Adana Demirspor	20	2	2	16	17:45	-28	5
