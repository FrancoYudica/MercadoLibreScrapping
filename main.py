from search_scrapper import SearchScrapper
from product_scrapper import ProductScrapper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import List, Dict
import json

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

    # Scraps search, and gathers product URLs
    scrapper = SearchScrapper()

    print("--- SCRAPING SEARCH ---")
    scrapper.scrap_search(search, 10)

    # WebDriver, required when scrapping products
    webdriver = create_webdriver()

    # Loads NamedXPaths from disk
    named_x_paths = dict()
    with open("NamedXPaths.json", "r") as file:
        named_x_paths = json.load(file)

    # Scraps all the products
    print("--- SCRAPING PRODUCTS ---")

    products: List[SearchScrapper] = scrap_products(
        scrapper.products_url, 
        webdriver, 
        named_x_paths, 
        False)
    
    print("--- ALL PRODUCTS SCRAPPED ---")

    # Creates a set containing the data labels of the products
    all_product_attributes = set()
    for product in products:
        for attribute in product.data.keys():
            all_product_attributes.add(attribute)


    for attribute in all_product_attributes:
        for product in products:
            print(attribute, product.data[attribute] if attribute in product.data else None)

