import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_udisc_courses(page_number):
    url = f"https://udisc.com/courses?lat=38.7413652&lng=-92.0005231&swLat=13.5003858&swLng=-136.1129719&neLat=57.4488811&neLng=-47.8880743&zoom=3.1476802&page={page_number}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        ul = soup.find('ul', class_='divide-divider border-divider mt-2 flex-1 flex-col divide-y border-y')
        if ul:
            return ul.find_all('li')
        else:
            print("Failed to find the unordered list on the page.")
            return None
    else:
        print("Failed to fetch data from the page:", url)
        return None

def extract_data_from_element(li):
    classes = ['text-lg font-bold', 'text-subtle mt-1 flex items-center text-base', 'mt-1 text-sm', 'mt-3']
    data = {}
    for i, class_name in enumerate(classes, start=1):
        element = li.find(class_=class_name)
        if element:
            data[str(i)] = element.text.strip()
        else:
            data[str(i)] = None
    return data

def save_to_excel(entries, filename):
    data = [extract_data_from_element(entry) for entry in entries]
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    print(f"Data saved to {filename}")

def main():
    total_pages = 501
    for page_number in range(362, total_pages + 1):
        entries = scrape_udisc_courses(page_number)
        if entries:
            save_to_excel(entries, f"udisc_courses_page_{page_number}.xlsx")

if __name__ == "__main__":
    main()
