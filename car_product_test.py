from product_scrapper import ProductScrapper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if __name__ == "__main__":
    test_url = "https://auto.mercadolibre.com.ar/MLA-1429720177-volkswagen-vento-25-luxury-170cv-tiptronic-2016-_JM#position=2&search_layout=grid&type=item&tracking_id=f777b562-def8-46df-9b51-cb9926a6a5c7"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    product = ProductScrapper(test_url, driver)

    x_paths = {
        "name": "/html/body/main/div[2]/div[5]/div/div[1]/div/div[1]/div/div[1]/div/div[2]/h1",
        "price": "/html/body/main/div[2]/div[5]/div/div[1]/div/div[1]/div/div[2]/div/div/div/span/span/span[2]",
        "other": "/html/body/main/div[2]/div[5]/div/div[1]/div/div[2]/div[1]/div/ul/div[4]/div/p",
        "brand": "/html/body/main/div[2]/div[5]/div/div[2]/div[2]/div[1]/section/div[3]/div/div/div/div[1]/div[1]/table/tbody/tr[1]/td/span"
    }

    product.scrap_x_paths(x_paths)
    product.scrap_features_tables()

    print(product.data)

    driver.quit()