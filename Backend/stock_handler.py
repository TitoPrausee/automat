"""
Stock Management
=================
This module handles the management of product stock, including adding,
removing, importing, and exporting products using CSV files.
"""

import csv  # Module for working with CSV files
import os   # Module for working with operating system functions

class Produkt:
    """
    Represents a single product with name, price, and quantity.

    Attributes:
        name (str): The name of the product.
        preis (float): The price of the product.
        menge (int): The quantity of the product in stock.
    """
    def __init__(self, name, preis, menge):
        self.name = name  # Name of the product
        self.preis = preis  # Price of the product
        self.menge = menge  # Quantity of the product

class Bestand:
    """
    Manages a collection of products in stock.

    Methods:
        add_produkt(produkt): Adds a product to the stock.
        remove_produkt(name, menge): Removes a specific quantity of a product from the stock.
        get_produkt(name): Retrieves a product by its name.
        __str__(): Returns a readable representation of the stock.
        import_from_csv(filename): Imports products from a CSV file.
        export_to_csv(filename): Exports the current stock to a CSV file.
    """
    def __init__(self):
        self.produkte = {}  # Dictionary to store products by name

    def add_produkt(self, produkt):
        """
        Add a product to the stock. If the product already exists, 
        increase its quantity.

        :param produkt: An instance of the Produkt class to be added to stock.
        """
        if produkt.name in self.produkte:
            # If the product exists, increase the quantity
            self.produkte[produkt.name].menge += produkt.menge
        else:
            # If the product does not exist, add it to the stock
            self.produkte[produkt.name] = produkt

    def remove_produkt(self, name, menge):
        """
        Remove a specific quantity of a product from the stock.

        :param name: The name of the product to be removed.
        :param menge: The quantity to be removed.
        """
        if name in self.produkte:
            # Check if there is enough stock to remove the requested quantity
            if self.produkte[name].menge >= menge:
                self.produkte[name].menge -= menge
            else:
                print("Nicht genug Produkte auf Lager.")
        else:
            print("Produkt nicht gefunden.")

    def get_produkt(self, name):
        """
        Retrieve a product by its name.

        :param name: The name of the product to retrieve.
        :return: The Produkt instance if found, else None.
        """
        return self.produkte.get(name)

    def __str__(self):
        """
        Return a readable representation of the current stock.

        :return: A string showing all products and their quantities.
        """
        output = "Bestand:\n"
        for produkt in self.produkte.values():
            output += f"{produkt.name}: {produkt.menge} Stück\n"
        return output

    def import_from_csv(self, filename):
        """
        Import products from a CSV file into the stock.

        :param filename: The name of the CSV file to import from.
        """
        filepath = os.path.join('CSV', filename)
        with open(filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # Unpack each row to get product details
                name, preis, menge = row
                produkt = Produkt(name, float(preis), int(menge))
                self.add_produkt(produkt)

    def export_to_csv(self, filename):
        """
        Export the current stock to a CSV file.

        :param filename: The name of the CSV file to export to.
        """
        filepath = os.path.join('CSV', filename)
        with open(filepath, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for produkt in self.produkte.values():
                # Write each product's details to the CSV file
                writer.writerow([produkt.name, produkt.preis, produkt.menge])
