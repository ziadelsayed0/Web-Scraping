import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_pdga_players(page_number):
    url = f"https://www.pdga.com/players?page={page_number}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table', {'class': 'views-table'})
        if table:
            rows = table.find_all('tr')

            data = []
            for row in rows[1:]:
                cells = row.find_all('td')
                player_data = [cell.text.strip() for cell in cells]
                data.append(player_data)

            return data
    return None

def scrape_all_pdga_players(start_page, total_pages):
    all_data = []
    for page_number in range(start_page, total_pages + 1):
        page_data = scrape_pdga_players(page_number)
        if page_data:
            all_data.extend(page_data)
        time.sleep(1)  # Adding a delay of 1 second between requests to be respectful to the server
    return all_data

def save_to_excel(data, filename):
    df = pd.DataFrame(data, columns=['Name', 'PDGA #', 'Rating' , 'Class', 'City', 'State/Prov', 'Country', 'Membership Status'])
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    start_page = 10856
    total_search = 343  # Specify the same page number
    all_player_data = scrape_all_pdga_players(start_page, start_page + total_search - 1)
    save_to_excel(all_player_data, f'pdga_players_page_{start_page}.xlsx')
