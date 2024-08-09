"""
Price Calculator
================
This module handles price calculation by loading data from a CSV file and 
providing functions to calculate and display the total price of items.
"""

import csv
import os

# Constants for file paths
CSV_DIR = 'CSV'  # Directory where CSV files are stored
PRICES_FILE = 'prices.csv'  # Filename for the prices data

# Price data storage
prices_data = {}  # Dictionary to store prices loaded from the CSV file


def load_prices_from_csv():
    """
    Load prices from the CSV file into the prices_data dictionary.

    This function reads the CSV file containing item prices and populates 
    the global prices_data dictionary with item names as keys and their 
    respective prices as values.
    """
    csv_file_path = os.path.join(CSV_DIR, PRICES_FILE)
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Store each item and its price in the dictionary
            prices_data[row['name']] = float(row['price'])


def calculate_total_price(item_name, quantity):
    """
    Calculate the total price for a given item and quantity.

    :param item_name: Name of the item to be priced.
    :param quantity: Number of units of the item.
    :return: Total price for the specified quantity of the item.
    """
    if item_name in prices_data:
        # Calculate total by multiplying the item price by the quantity
        return prices_data[item_name] * quantity
    else:
        # If item is not found, return 0.0 as the price
        return 0.0


def display_price(total_price):
    """
    Display the total price formatted to two decimal places.

    :param total_price: The total price to be displayed.
    """
    print(f"Total Price: {total_price:.2f} €")
