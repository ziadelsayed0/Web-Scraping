import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape all tables from the URL
def scrape_events(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', class_='views-table cols-7')

    # Initialize lists to store data
    names = []
    dates = []
    statuses = []
    classes = []
    tiers = []
    locations = []

    # Loop through all tables on the page
    for table in tables:
        # Loop through rows in the table and extract data
        for row in table.find_all('tr')[1:]:  # Skip the header row
            columns = row.find_all('td')

            # Extract data from each column
            name = columns[0].text.strip()
            date = columns[1].text.strip()
            status = columns[2].text.strip()
            class_ = columns[3].text.strip()
            tier = columns[4].text.strip()
            location = columns[5].text.strip()

            # Append data to lists
            names.append(name)
            dates.append(date)
            statuses.append(status)
            classes.append(class_)
            tiers.append(tier)
            locations.append(location)

    return names, dates, statuses, classes, tiers, locations

# Function to save data to a single Excel sheet for all months
def save_to_excel(names_list, dates_list, statuses_list, classes_list, tiers_list, locations_list):
    data = {
        'Name': names_list,
        'Date': dates_list,
        'Status': statuses_list,
        'Class': classes_list,
        'Tier': tiers_list,
        'Location': locations_list
    }
    df = pd.DataFrame(data)
    filename = 'leagues_events_all_months.xlsx'
    df.to_excel(filename, index=False)
    print(f'Data saved to {filename}')

# Main function
def main():
    base_url = 'https://www.pdga.com/leagues/events/2024'
    months = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

    # Initialize lists to store data for all months
    all_names = []
    all_dates = []
    all_statuses = []
    all_classes = []
    all_tiers = []
    all_locations = []

    for month in months:
        url = f'{base_url}/{month}'
        names, dates, statuses, classes, tiers, locations = scrape_events(url)

        # Append data for current month to the lists for all months
        all_names.extend(names)
        all_dates.extend(dates)
        all_statuses.extend(statuses)
        all_classes.extend(classes)
        all_tiers.extend(tiers)
        all_locations.extend(locations)

    # Save data for all months to a single Excel sheet
    save_to_excel(all_names, all_dates, all_statuses, all_classes, all_tiers, all_locations)

if __name__ == "__main__":
    main()
