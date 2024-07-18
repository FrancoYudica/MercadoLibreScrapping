from src.search_scrapper import SearchScrapper
from src.product_scrapper import ProductScrapper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import List, Dict
from src.sheet_exporter import export_to_sheets
from datetime import datetime
import json
import time
import argparse
from pathlib import Path

def create_webdriver(headless: bool):
    options = Options()
    
    if headless:
        # Run Chrome in headless mode (without a GUI)
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    
    # Disable the use of /dev/shm (shared memory) to prevent out-of-space issues
    options.add_argument('--disable-dev-shm-usage') 
    
    # Initialize and return the Chrome WebDriver with the specified options
    return webdriver.Chrome(options=options)

def scrap_products(
        urls: List[str], 
        webdriver,
        x_paths: Dict[str, str],
        scrap_features_table: bool = True,
        max_image_count: int = 1
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

        # Scraps images if possible
        product_scrapper.scrap_images(max_image_count)

        # Only adds product if it was correctly scrapped
        if success:
            products.append(product_scrapper)

    return products

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Scrap Mercado Libre products and export to CSV.')
    parser.add_argument('--table', action='store_true', help='Include this flag to scrap the features table')
    parser.add_argument('--show_browser', action='store_true', help='Include this flag to scrap with browser UI')
    parser.add_argument('--xpaths_file', type=str, help='Path to the JSON file containing the named XPaths')
    parser.add_argument('--images', type=int, help='Sets the maximum amount of scrapped product images')
    args = parser.parse_args()
    search: str = input("Search in mercado libre: ")
    amount: int = int(input("How many products do you want to search?: "))

    start_time = time.time()

    # Scraps search, and gathers product URLs
    scrapper = SearchScrapper()

    print("--- SCRAPING SEARCH ---")
    scrapper.scrap_search(search, amount)

    # WebDriver, required when scrapping products
    webdriver = create_webdriver(not args.show_browser)

    named_x_paths = dict()
    
    # Loads NamedXPaths from disk
    if args.xpaths_file is not None:
        
        # In case folder "product_xpaths" is omitted
        path = Path(args.xpaths_file)
        if not path.exists():
            path = Path("product_xpaths") / args.xpaths_file

        with open(path, "r") as file:
            named_x_paths = json.load(file)

    # Scraps all the products
    print("--- SCRAPING PRODUCTS ---")

    products: List[ProductScrapper] = scrap_products(
        scrapper.products_url, 
        webdriver, 
        named_x_paths, 
        args.table,
        args.images if args.images is not None else 1)
    
    print("--- EXPORTING TO SHEET ---")

    # Sets output filename with current datetime
    now = datetime.today()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    output_directory = Path("output")
    output_directory.mkdir(parents=True, exist_ok=True)
    filename = f"{dt_string}({search})(n={amount}).csv"
    filepath = output_directory / filename

    export_to_sheets(filepath, products)

    print(f"--- COMPLETED IN {time.time() - start_time} SECONDS ---")
    print(f"Results saved in file: {filename}")
