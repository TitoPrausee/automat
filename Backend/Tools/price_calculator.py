
"""
Price Calculator
================
"""
import csv
import os
from DataAccessors.Price import Price

# Constants
CSV_DIR = 'CSV'
PRICES_FILE = 'prices.csv'


def calculate_total_price(item_name, quantity):
    """Calculate total price based on item name and quantity"""
    prices_data = Price.readAllPrices()
    if item_name in prices_data:
        return prices_data[item_name] * quantity
    else:
        return 0.0

def display_price(total_price):
    """Display the total price with two decimal places"""
    print(f"Total Price: {total_price:.2f} €")

if __name__ == '__main__':
    total_price = calculate_total_price('cola', 2)
    display_price(total_price)

    #---