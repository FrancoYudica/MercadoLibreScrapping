from bs4 import BeautifulSoup
import requests

class SearchScrapper:
    """
    Collects a set of URL from Mercado Libre search
    """
    def __init__(self) -> None:
        self.products_url = set()
        self.scrapped_count = 0


    def scrap_search(self, search: str, target_product_count=10):
        spaces_replaced_search = search.replace(" ", "-")
        url = f"https://listado.mercadolibre.com.ar/{spaces_replaced_search}#D[A:{search}]"
        self.target_product_count = target_product_count
        self._scrap_pages(url)

    def _scrap_page_products(self, soup: BeautifulSoup):

        all_div = soup.find_all("div", {"class": "ui-search-item__group ui-search-item__group--title"})

        element_index = 0
        while (self.scrapped_count < self.target_product_count and element_index < len(all_div)):
            div_element = all_div[element_index]
            element_index += 1

            # Access link element <a></a>
            a_element = div_element.find("a", {"class": "ui-search-item__group__element ui-search-link__title-card ui-search-link"})
            url = a_element.get("href")
            self.products_url.add(url)
            self.scrapped_count += 1

            progress = int(self.scrapped_count / self.target_product_count * 100.0)
            print(f" > {progress}%. Added URL: {url}")


    def _scrap_pages(self, source_url):
        
        url = source_url
        self.scrapped_count = 0
        self.products_url.clear()

        while (self.scrapped_count < self.target_product_count):
            
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


if __name__ == "__main__":
    search: str = input("Search in mercado libre: ")
    scrapper = SearchScrapper()
    scrapper.scrap_search(search, 10)
