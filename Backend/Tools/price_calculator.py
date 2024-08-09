"""
Price Calculator
================
This module handles price calculation by loading data from a CSV file and 
providing functions to calculate and display the total price of items.
"""

import csv
import os
from DataAccessors.Price import Price

# Constants
CSV_DIR = 'CSV'  # Directory where CSV files are stored
PRICES_FILE = 'prices.csv'  # Filename for the prices data

# Global price data storage
_prices_data = None  # Lazy-loaded dictionary to store prices from CSV

def _load_prices_from_csv():
    """
    Load prices from the CSV file into the _prices_data dictionary.

    Reads the CSV file containing item prices and populates the global 
    _prices_data dictionary with item names as keys and their respective 
    prices as values.
    """
    global _prices_data
    if _prices_data is None:
        _prices_data = {}
        csv_file_path = os.path.join(CSV_DIR, PRICES_FILE)
        try:
            with open(csv_file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    _prices_data[row['name']] = float(row['price'])
        except (FileNotFoundError, KeyError) as e:
            print(f"Error loading prices from CSV: {e}")
            _prices_data = {}

def _merge_prices_with_additional_data():
    """
    Merge the CSV prices data with additional data from the Price module.

    Combines the prices from the CSV file with those from the Price module,
    with CSV data taking precedence if there are conflicts.
    """
    _load_prices_from_csv()  # Ensure CSV data is loaded
    additional_prices_data = Price.readAllPrices()
    all_prices_data = {**additional_prices_data, **_prices_data}
    return all_prices_data

def calculate_total_price(item_name, quantity):
    """
    Calculate the total price for a given item and quantity.

    :param item_name: Name of the item to be priced.
    :param quantity: Number of units of the item.
    :return: Total price for the specified quantity of the item.
    """
    all_prices_data = _merge_prices_with_additional_data()

    if item_name in all_prices_data:
        return all_prices_data[item_name] * quantity
    else:
        print(f"Item '{item_name}' not found. Returning price as 0.0 €.")
        return 0.0

def display_price(total_price):
    """
    Display the total price formatted to two decimal places.

    :param total_price: The total price to be displayed.
    """
    print(f"Total Price: {total_price:.2f} €")

if __name__ == '__main__':
    item_name = 'cola'
    quantity = 2
    total_price = calculate_total_price(item_name, quantity)
    display_price(total_price)
