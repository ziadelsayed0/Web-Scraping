import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_pdga_players(page_number):
    url = f"https://www.pdga.com/tour/search?date_filter[min][date]=2024-01-01&date_filter[max][date]=2024-12-31&page={page_number}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', {'class': 'views-table'})
        if table:
            rows = table.find_all('tr')

            data = []
            for row in rows[1:]:  # Skipping the header row
                cells = row.find_all('td')
                player_data = [cell.text.strip() for cell in cells]
                data.append(player_data)

            return data
    return None

def scrape_all_pdga_players(total_pages):
    all_data = []
    for page_number in range(total_pages):
        page_data = scrape_pdga_players(page_number)
        if page_data:
            all_data.extend(page_data)
        time.sleep(0.02)  # Adding a delay of 1 second 
    return all_data

def save_to_excel(data, filename):
    df = pd.DataFrame(data, columns=['Name', 'Status', 'Class', 'Tier', 'Tournament', 'Asst. Tournament Director', 'Location', 'Dates'])
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    total_pages = 3912
    all_search_data = scrape_all_pdga_players(total_pages)
    save_to_excel(all_search_data, 'search.xlsx')
