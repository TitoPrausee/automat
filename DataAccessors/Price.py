import csv  # Module for working with CSV files
import os   # Module for working with operating system functionalities

# 1. Class to manage price data
class Price:
    """
    Handles reading and updating prices from and to a CSV file.

    Attributes:
        _dirname: Directory path to the location of the CSV file.
        _csvPath: Full path to the prices CSV file.
    """

    # 1.1 Static attributes for paths
    _dirname = os.path.dirname(os.path.dirname(__file__))  # Directory name for the CSV directory
    _csvPath = os.path.join(_dirname, 'CSV/price.csv')  # Full path to the CSV file

    # 1.2 Method to read all prices from the CSV file
    @staticmethod
    def readAllPrices():
        """
        Reads all prices from the CSV file and returns them as a dictionary.

        :return: A dictionary with product names as keys and prices as values.
        """
        pricesData = {}  # Dictionary to store product names and their prices
        with open(Price._csvPath, "r", newline='') as csvFile:
            reader = csv.DictReader(csvFile)
            # Iterate through each row and store the product name and price as a float
            for row in reader:
                pricesData[row['name']] = float(row['price'])  # Store price as a float

        return pricesData  # Return the dictionary containing product prices

    # 1.3 Method to update the price of a product in the CSV file
    @staticmethod
    def updatePrice(name, price):
        """
        Updates the price of a specific product in the CSV file.

        :param name: The name of the product to update.
        :param price: The new price of the product.
        """
        # Check if the CSV file exists
        if not os.path.isfile(Price._csvPath):
            return

        # Read all data from the CSV file
        with open(Price._csvPath, "r", newline='') as csvFile:
            reader = csv.DictReader(csvFile)
            priceData = list(reader)  # Convert the reader object to a list for easier manipulation

        # Create a dictionary of current prices
        priceDict = {item['name']: float(item['price']) for item in priceData}

        # Update the price for the specified product
        if name in priceDict:
            priceDict[name] = price

        # Prepare the updated price data for writing back to the CSV file
        updatedPriceData = [{'name': name, 'price': price} for name, price in priceDict.items()]

        # Write the updated data back to the CSV file
        with open(Price._csvPath, "w", newline='') as csvFile:
            fieldnames = ['name', 'price']
            writer = csv.DictWriter(csvFile, fieldnames)
            writer.writeheader()  # Write the header row (name, price)
            for item in updatedPriceData:
                writer.writerow(item)  # Write each product's name and updated price