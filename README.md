# Ad Scraper for Divar.ir

This project scrapes real estate ad listings from `divar.ir` for the city of Babolsar.

## Brief Explanation of Scraping Strategy

The scraping process is implemented using Python with the Selenium library for web browser automation. Here's a step-by-step breakdown:

1.  **URL Generation (`menu.py`):**
    * An interactive command-line menu prompts the user to select a specific real estate category (e.g., "buy-residential," "rent-apartment") for Babolsar.
    * Based on the user's selection, a target URL for `divar.ir` is constructed.

2.  **Browser Initialization (`main.py` - `initialize_driver`):**
    * A headless Chrome WebDriver instance is initialized using `Selenium`.
    * Headless mode allows the browser to run in the background without a visible UI, which is efficient for scraping.
    * A standard user-agent string is set to mimic a regular browser visit, potentially reducing the chances of being blocked.

3.  **Page Navigation and Initial Load (`main.py` - `scroll_and_extract_ads`):**
    * The script navigates to the generated URL.
    * It waits for a specific main content container element (identified by class name `content-dd848`) to be present on the page before proceeding.

4.  **Dynamic Content Loading (Infinite Scrolling and "Load More" Button):**
    * **Scrolling:** The script simulates user scrolling within the identified content container. It repeatedly scrolls down by a fixed pixel amount (`1000px`) to trigger the loading of more ads, as `divar.ir` uses infinite scrolling.
    * **"Load More" Button:** If scrolling down does not load new ads after a few attempts, the script actively looks for a "Load More" button (class `post-list__load-more-btn-be092`). If found and visible, it clicks this button using JavaScript execution to load additional batches of ads.
    * **Pauses:** Short pauses (`time.sleep`) are implemented after each scroll action and "Load More" click to allow the new content to fully load on the page.

5.  **Ad Element Identification and Data Extraction (`main.py` - `scroll_and_extract_ads`, `extract_ad_data`):**
    * After each scroll or "Load More" action, the script finds all ad container elements (identified by class name `post-list__items-container-e44b2`).
    * To prevent duplicate entries, each ad is identified by its `data-index` attribute. A `set` of `seen_indexes` tracks ads already processed.
    * For each new ad container, the `extract_ad_data` function is called. This function attempts to locate and extract specific pieces of information from within the ad element using their respective class names:
        * Title (`unsafe-kt-post-card__title`)
        * Deposit (first `unsafe-kt-post-card__description`)
        * Rent (second `unsafe-kt-post-card__description`)
        * Agency (`unsafe-kt-post-card__bottom-description`)
        * Direct link to the ad (the `href` attribute of `unsafe-kt-post-card__action`)
    * If a particular piece of information is not found for an ad, it defaults to "N/A".

6.  **Termination Conditions (`main.py` - `scroll_and_extract_ads`):**
    * The scraping process stops under one of the following conditions:
        * A predefined maximum number of scroll attempts (`max_scrolls`) is reached.
        * No new ads are loaded, and the "Load More" button is not found or clickable for a consecutive number of attempts (`max_no_change_rounds`). This indicates that all available ads have likely been loaded.

7.  **Data Storage (`main.py` - `save_to_file`):**
    * Once the scraping is complete, all collected ad data (stored as a dictionary with `data-index` as keys) is saved into a JSON file named `output.json`.

8.  **Resource Management (`main.py` - `main`):**
    * The WebDriver instance is properly closed (`driver.quit()`) in a `finally` block to ensure browser processes are terminated, even if errors occur during scraping.

This strategy is designed to handle dynamically loaded content and extract structured data from the ad listings.
