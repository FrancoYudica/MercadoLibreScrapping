import csv
from typing import List
from src.product_scrapper import ProductScrapper
from pathlib import Path

def export_to_sheets(filepath: Path, products: List[ProductScrapper]):

    # Creates a set containing the data labels of the products
    all_product_attributes = set()
    for product in products:
        for attribute in product.data.keys():
            all_product_attributes.add(attribute)

    # Gets the data of all the products, as column mayor
    products_data = []

    # Gets all the data by columns
    for attribute in all_product_attributes:
        
        attribute_column = [attribute]

        for product in products:

            if attribute in product.data:
                attribute_column.append(product.data[attribute])
            else:
                attribute_column.append(None)

        products_data.append(attribute_column)

    # Sorts the columns by the amount of not null occurrences
    def not_null_count(column: list):
        return len(column) - column.count(None)

    sorted_products_data = sorted(products_data, key=not_null_count, reverse=True)

    # Transform column-major matrix to row-major matrix
    row_major_data = list(zip(*sorted_products_data))

    # Write data to CSV
    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_major_data)
