from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import requests
import time

# Path to your chromedriver
chrome_driver_path = 'driver/chromedriver-win64/chromedriver.exe'

# Set download preferences
download_directory = os.path.abspath('.')  # Download to the current directory
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": download_directory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
})

# Create a new Chrome driver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # URL
    driver.get('https://shepardes.com/event-services/technology/floor-plan-search/')

    select_container = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.select2-container'))
    )

    print("Opening dropdown...")
    select_container.click()

    ul_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//ul[@class='select2-results__options']"))
    )
    print("Dropdown options loaded.")

    # Find all list items within the unordered list
    options = ul_element.find_elements(By.TAG_NAME, "li")

    # Iterate over each option, starting from the second item
    for index in range(1, len(options)):
        select_container.click()

        ul_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//ul[@class='select2-results__options']"))
        )

        options = ul_element.find_elements(By.TAG_NAME, "li")

        print(f"Selecting option {index}: {options[index].text}")
        options[index].click()

        table = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'table'))
        )

        # Locate the PDF link in the table and get its URL
        pdf_links = table.find_elements(By.XPATH, './/a[contains(@href, ".pdf")]')

        for pdf_link in pdf_links:
            pdf_link_url = pdf_link.get_attribute('href')

            # Download the PDF using requests
            response = requests.get(pdf_link_url)
            pdf_filename = os.path.join(download_directory, pdf_link_url.split('/')[-1])
            with open(pdf_filename, 'wb') as file:
                file.write(response.content)

            print(f'PDF downloaded successfully: {pdf_filename}')

        # Add a small delay to avoid overwhelming the server
        time.sleep(2)

finally:
    # Close the browser
    driver.quit()
