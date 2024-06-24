from bs4 import BeautifulSoup
import requests

def scrap_page_products(soup: BeautifulSoup):

    all_div = soup.find_all("div", {"class": "ui-search-item__group ui-search-item__group--title"})
    products = []
    for item in all_div:
        product_data = {}

        # Access link element <a></a>
        a_element = item.find("a", {"class": "ui-search-item__group__element ui-search-link__title-card ui-search-link"})
        product_data["name"] = a_element.text
        product_data["href"] = a_element.get("href")
        print(product_data["name"])
        products.append(product_data)

def scrap_pages(source_url, max_pages=3):
    
    url = source_url

    for _ in range(max_pages):
        print(f"Scrapping url: {url}")
        # Gets html
        get_request = requests.get(url)
        soup = BeautifulSoup(get_request.content, "html.parser")
        scrap_page_products(soup)

        # Finds next button
        li_next_element = soup.find("li", {"class": "andes-pagination__button andes-pagination__button--next"})

        # There isn't any other next button. Search completed
        if li_next_element is None:
            break
        
        # Access url of next page
        a_element = li_next_element.find("a")
        url = a_element.get("href")

def scrap_search(search):
    spaces_replaced_search = search.replace(" ", "-")
    url = f"https://listado.mercadolibre.com.ar/{spaces_replaced_search}#D[A:{search}]"


    scrap_pages(url, 100)

if __name__ == "__main__":

    search: str = input("Search in mercado libre: ")
    scrap_search(search)
