from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


def init_driver():
    options= Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('user-agent=Mozilla/5.0')

    driver=webdriver.Chrome(options=options)
    return driver


def get_year_links(driver):
    # driver=init_driver()

    driver.get('https://www.baseball-almanac.com/yearmenu.shtml')
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "td.datacolBox a"))
    )
 
    links =driver.find_elements(By.CSS_SELECTOR, "td.datacolBox a")

    year_links =[]
    for link in links:
        year_text = link.text.strip()
        href= link.get_attribute('href')
        if year_text.isdigit() and href:
            year_links.append((year_text, href))

    return year_links   

def scrape_year_page(driver, year, url):
    driver.get(url)
    time.sleep(2)

    rows = []
    tables = driver.find_elements(By.CSS_SELECTOR, "div.ba-table")

    for table in tables:
        try:
            event_name_elem = table.find_element(By.CSS_SELECTOR, "h2")
            event_name = event_name_elem.text.strip()

            stat_rows = table.find_elements(By.CSS_SELECTOR, "table.boxed tr")

            for row in stat_rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if not cells:
                    continue


                stat_text = " | ".join([cell.text.strip() for cell in cells if cell.text.strip()])
                if stat_text:
                    rows.append((year, event_name, stat_text))

        except Exception as e:
            print(f"Error in year {year}: {e}")
            continue

    print(f" Scraped {len(rows)} rows from {year}") 
    return rows
    

def run_full_scraper():
    driver = init_driver()
    all_data = []
    try:
        print(" Getting year links...") 
        year_links = get_year_links(driver)
        print(f"Found {len(year_links)} years.")

        for year, url in year_links[:10]: 
            print(f" Scraping {year}...") 
            try:
                year_data = scrape_year_page(driver, year, url)
                all_data.extend(year_data)
            except Exception as e:
                print(f"Failed to scrape {year}: {e}")

            time.sleep(2)

    finally:
        driver.quit()
    if not all_data:
        print(" No data scraped.") 
        return
    os.makedirs("raw-data", exist_ok=True)
    df = pd.DataFrame(all_data, columns=["Year", "Event", "Stat"])    
    df.to_csv("raw-data/mlb_history.csv", index=False)
    print(" Data scraped and saved to raw-data/mlb_history.csv")


if __name__ == "__main__":
    run_full_scraper()

