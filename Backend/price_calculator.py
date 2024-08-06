

"""
Price Calculator
================

"""

import csv
import os

# Constants
CSV_DIR = 'CSV'
PRICES_FILE = 'prices.csv'

# Price data storage
prices_data = {}

def load_prices_from_csv():
    """Load prices from CSV file"""
    csv_file_path = os.path.join(CSV_DIR, PRICES_FILE)
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            prices_data[row['name']] = float(row['price'])

def calculate_total_price(item_name, quantity):
    """Calculate total price based on item name and quantity"""
    if item_name in prices_data:
        return prices_data[item_name] * quantity
    else:
        return 0.0

def display_price(total_price):
    """Display the total price with two decimal places"""
    print(f"Total Price: {total_price:.2f} €")

if __name__ == '__main__':
    load_prices_from_csv()
    total_price = calculate_total_price('cola', 2)
    display_price(total_price)

    # ---