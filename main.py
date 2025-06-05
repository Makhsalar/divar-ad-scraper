# MIT License
# Copyright (c) 2025 Makhsalar
# See LICENSE file in the root of this project for license information.

"""Module for scraping ads from a given URL using Selenium."""

import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from menu import display_menu_and_get_url


def initialize_driver():
    """Initializes and returns a headless Chrome WebDriver instance."""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    )

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )


def extract_ad_data(wrapper):
    """Extracts and returns a dictionary of ad data from a wrapper element."""
    try:
        title_element = wrapper.find_element(
            By.CLASS_NAME, "unsafe-kt-post-card__title"
        )
    except NoSuchElementException:
        title_element = None

    description_elements = wrapper.find_elements(
        By.CLASS_NAME, "unsafe-kt-post-card__description"
    )
    agency_elements = wrapper.find_elements(
        By.CLASS_NAME, "unsafe-kt-post-card__bottom-description"
    )
    link_elements = wrapper.find_elements(By.CLASS_NAME, "unsafe-kt-post-card__action")

    return {
        "title": title_element.text.strip() if title_element else "N/A",
        "deposit": (
            description_elements[0].text.strip()
            if len(description_elements) > 0
            else "N/A"
        ),
        "rent": (
            description_elements[1].text.strip()
            if len(description_elements) > 1
            else "N/A"
        ),
        "agency": (
            agency_elements[0].text.strip() if len(agency_elements) > 0 else "N/A"
        ),
        "link": (
            link_elements[0].get_attribute("href") if len(link_elements) > 0 else "N/A"
        ),
    }


def click_load_more(driver, scroll_pause_time):
    """Clicks the 'Load More' button if found and returns True. Else returns False."""
    try:
        load_more_button = driver.find_element(
            By.CLASS_NAME, "post-list__load-more-btn-be092"
        )
        if load_more_button.is_displayed():
            print("➡️  'Load More' button found. Clicking...")
            driver.execute_script("arguments[0].click();", load_more_button)
            time.sleep(scroll_pause_time * 2)
            return True
    except NoSuchElementException:
        print("❌ 'Load More' button not found or not clickable.")
    return False


def scroll_and_extract_ads(driver, url):
    """Scrolls the page and extracts ad data."""
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    scroll_container = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "content-dd848"))
    )

    seen_indexes = set()
    data = {}
    scroll_pause_time = 2.5
    max_scrolls = 1000
    max_no_change_rounds = 3
    no_change_rounds_counter = 0

    for scroll_num in range(max_scrolls):
        print(f"\n[Scroll {scroll_num + 1}/{max_scrolls}] Scrolling...")
        driver.execute_script("arguments[0].scrollTop += 1000", scroll_container)
        time.sleep(scroll_pause_time)

        ad_wrappers = driver.find_elements(
            By.CLASS_NAME, "post-list__items-container-e44b2"
        )
        print(f"Detected {len(ad_wrappers)} wrappers")

        new_ads_count = 0
        for wrapper in ad_wrappers:
            data_index = wrapper.get_attribute("data-index")
            if not data_index or data_index in seen_indexes:
                continue
            seen_indexes.add(data_index)
            new_ads_count += 1
            data[data_index] = extract_ad_data(wrapper)

        print(f"New ads this scroll: {new_ads_count}")

        if new_ads_count == 0:
            print("No new ads. Checking for 'Load More' button...")
            if click_load_more(driver, scroll_pause_time):
                continue
            no_change_rounds_counter += 1
            print(
                f"No new ads detected. No-change rounds: "
                f"{no_change_rounds_counter}/{max_no_change_rounds}"
            )
            if no_change_rounds_counter >= max_no_change_rounds:
                print("No more content loading. Ending scroll.")
                break
        else:
            no_change_rounds_counter = 0

    return data


def save_to_file(data, path="output.json"):
    """Saves the collected ad data to a JSON file."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def main():
    """Main entry point for ad scraper."""
    url = display_menu_and_get_url()
    print(f"Target URL: {url}")

    driver = None
    try:
        driver = initialize_driver()
        print("Driver initialized. Starting scraping...")
        data = scroll_and_extract_ads(driver, url)
    finally:
        if driver:
            print("Closing browser.")
            driver.quit()

    save_to_file(data)
    print(f"\n✅ Scraping completed. Total ads saved: {len(data)}")


if __name__ == "__main__":
    main()
