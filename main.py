from src.search_scrapper import SearchScrapper
from src.product_scrapper import ProductScrapper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import List, Dict
from src.sheet_exporter import export_to_sheets
import json
import time
from datetime import datetime

def create_webdriver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage') 
    
    return webdriver.Chrome(options=options)

def scrap_products(
        urls: List[str], 
        webdriver,
        x_paths: Dict[str, str],
        scrap_features_table: bool = True
        ) -> List[ProductScrapper]:
    
    # Iterates through all URLs and scraps the product
    products = []

    for i, product_url in enumerate(urls):
        progress = int(i / len(scrapper.products_url) * 100)
        print(f" > {progress}%. Scrapping product URL: {product_url}")

        product_scrapper = ProductScrapper(product_url, webdriver)
        
        # Executes GET petition
        product_scrapper.webdriver_url()
        # Scraps the specified XPaths
        success = product_scrapper.scrap_x_paths(x_paths)

        # Scraps the features table
        if scrap_features_table:
            success &= product_scrapper.scrap_features_tables()

        # Only adds product if it was correctly scrapped
        if success:
            products.append(product_scrapper)

    return products

if __name__ == "__main__":
    search: str = input("Search in mercado libre: ")
    amount: int = int(input("How many products do you want to search?: "))

    start_time = time.time()

    # Scraps search, and gathers product URLs
    scrapper = SearchScrapper()

    print("--- SCRAPING SEARCH ---")
    scrapper.scrap_search(search, amount)

    # WebDriver, required when scrapping products
    webdriver = create_webdriver()

    # Loads NamedXPaths from disk
    named_x_paths = dict()
    with open("NamedXPaths.json", "r") as file:
        named_x_paths = json.load(file)

    # Scraps all the products
    print("--- SCRAPING PRODUCTS ---")

    products: List[ProductScrapper] = scrap_products(
        scrapper.products_url, 
        webdriver, 
        named_x_paths, 
        True)
    
    print("--- EXPORTING TO SHEET ---")

    # Sets output filename with current datetime
    now = datetime.today()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    filename = f"results-{dt_string}.csv"

    export_to_sheets(filename, products)

    print(f"--- COMPLETED IN {time.time() - start_time} SECONDS ---")
    print(f"Results saved in file: {filename}")
