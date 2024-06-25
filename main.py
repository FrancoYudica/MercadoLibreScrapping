from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MercadoLibreScrapper:
    def __init__(self) -> None:
        self.products = []

    def scrap_search(self, search):
        spaces_replaced_search = search.replace(" ", "-")
        url = f"https://listado.mercadolibre.com.ar/{spaces_replaced_search}#D[A:{search}]"
        self._scrap_pages(url, 1)

        print(self.products)


    def _scrap_page_products(self, soup: BeautifulSoup) -> list:

        all_div = soup.find_all("div", {"class": "ui-search-item__group ui-search-item__group--title"})
        for item in all_div:
            product_data = {}

            # Access link element <a></a>
            a_element = item.find("a", {"class": "ui-search-item__group__element ui-search-link__title-card ui-search-link"})
            product_data["name"] = a_element.text
            product_data["href"] = a_element.get("href")
            # print(product_data["name"])
            self.products.append(product_data)


    def _scrap_pages(self, source_url, max_pages=3):
        
        url = source_url

        for _ in range(max_pages):
            print(f"Scrapping url: {url}")
            # Gets html
            get_request = requests.get(url)
            soup = BeautifulSoup(get_request.content, "html.parser")
            self._scrap_page_products(soup)

            # Finds next button
            li_next_element = soup.find("li", {"class": "andes-pagination__button andes-pagination__button--next"})

            # There isn't any other next button. Search completed
            if li_next_element is None:
                break
            
            # Access url of next page
            a_element = li_next_element.find("a")
            url = a_element.get("href")

    def _scrap_product_page(self, product, product_url):
        # Set up Selenium with headless Chrome
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)

        try:
            driver.get(product_url)


            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")
            button = soup.find("button", {"class": "ui-pdp-collapsable__action"})
            d = soup.find("div", {"class": "ui-pdp-container__row ui-pdp-container__row--technical-specifications"})
            div_specs = soup.find("div", {"class": "ui-vpp-striped-specs"})
            table_element = div_specs.find("table")
            table_body_element = table_element.find("tbody")

            table_row_elements = table_body_element.find_all("tr")
            print(table_row_elements)

            # TODO add all row elements to product

        finally:
            driver.quit()
    
    def _scrap_product_page_1(self, product, product_url):
        get_request = requests.get(product_url)
        soup = BeautifulSoup(get_request.content, "html.parser")
        div_specs = soup.find("div", {"class": "ui-pdp-container__row ui-pdp-container__row--technical-specifications"})
        btn_specs = soup.find("button", {"class": "ui-pdp-collapsable__action"})
        # div_specs = soup.find("div", {"class": "ui-vpp-striped-specs__table"})
        table_element = div_specs.find("table")
        table_body_element = table_element.find("tbody")

        table_row_elements = table_body_element.find_all("tr")
        print(table_row_elements)

        ## TODO add all row elements to product


if __name__ == "__main__":

    # search: str = input("Search in mercado libre: ")
    scrapper = MercadoLibreScrapper()
    scrapper._scrap_product_page_1({}, "https://auto.mercadolibre.com.ar/MLA-1429720177-volkswagen-vento-25-luxury-170cv-tiptronic-2016-_JM#position=2&search_layout=grid&type=item&tracking_id=f777b562-def8-46df-9b51-cb9926a6a5c7")
    # scrapper.scrap_search(search)
