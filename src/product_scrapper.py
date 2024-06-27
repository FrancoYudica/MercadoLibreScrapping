from lxml import etree
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from typing import Dict

class ProductScrapper:

    def __init__(self, url, webdriver: WebDriver) -> None:
        self.url: str = url
        self.webdriver: WebDriver = webdriver
        self.timeout = 10

        # Stores data classified by features
        self.data = {"url": self.url}

    def webdriver_url(self):
        self.webdriver.get(self.url)

    def scrap_x_paths(self, named_x_paths: Dict[str, str]) -> bool:
        self.webdriver.refresh()

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(self.webdriver.page_source, "html.parser")
        
        # Convert soup to lxml object for XPath queries
        dom = etree.HTML(str(soup))

        for name, x_path in named_x_paths.items():

            element = dom.xpath(x_path)

            if len(element) > 0:
                self.data[name] = element[0].text
            
            else:
                self.data[name] = None
        
        return True
      
    # Scraps all the features table and stores all attributes
    def scrap_features_tables(self) -> bool:

        # Wait for the button to be present and click it
        try:
            button = WebDriverWait(self.webdriver, self.timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "ui-pdp-collapsable__action"))
            )

            # Scroll element into view in order to click
            self.webdriver.execute_script("arguments[0].scrollIntoView();", button)

            button.click()

            # Wait for the div with the class "ui-vpp-striped-specs__table" to be present
            WebDriverWait(self.webdriver, self.timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "ui-vpp-striped-specs__table"))
            )
        except TimeoutException:
            print("Timed out waiting for button or specs table to load")
            return False

        # Get page source and parse with BeautifulSoup
        soup = BeautifulSoup(self.webdriver.page_source, "html.parser")

        # Gets all the divs that contains specs table
        div_specs = soup.find_all("div", {"class": "ui-vpp-striped-specs__table"})
        if not div_specs:
            print("Div with class 'ui-vpp-striped-specs__table' not found")
            return False
        
        for div_spec in div_specs:

            # And loads all the rows values
            for tr_element in div_spec.find_all("tr"):
                
                div_with_row_name = tr_element.find("div", {"class": "andes-table__header__container"})
                div_with_row_value = tr_element.find("span", {"class": "andes-table__column--value"})

                if div_with_row_name is None or div_with_row_value is None:
                    continue

                self.data[div_with_row_name.text] = div_with_row_value.text

        return True