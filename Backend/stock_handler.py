import csv
import os

# 1. Klasse zur Darstellung eines Produkts (ohne Preis)
class Produkt:
    """
    Represents a single product with name and quantity.

    Attributes:
        name (str): The name of the product.
        menge (int): The quantity of the product in stock.
    """
    def __init__(self, name, menge):
        self.name = name  # Name des Produkts
        self.menge = menge  # Menge des Produkts

# 2. Klasse zur Verwaltung des Bestands
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
        self.produkte = {}  # Speichert nur Produkte mit Namen und Mengen

    # 2.1 Produkt zum Bestand hinzufügen
    def add_produkt(self, produkt):
        """
        Add a product to the stock. If the product already exists, 
        increase its quantity.

        :param produkt: An instance of the Produkt class to be added to stock.
        """
        if produkt.name in self.produkte:
            self.produkte[produkt.name].menge += produkt.menge
        else:
            self.produkte[produkt.name] = produkt

    # 2.2 Produkt aus dem Bestand entfernen
    def remove_produkt(self, name, menge):
        """
        Remove a specific quantity of a product from the stock.

        :param name: The name of the product to be removed.
        :param menge: The quantity to be removed.
        """
        if name in self.produkte:
            if self.produkte[name].menge >= menge:
                self.produkte[name].menge -= menge
            else:
                print("Nicht genug Produkte auf Lager.")
        else:
            print("Produkt nicht gefunden.")

    # 2.3 Produkt anhand des Namens abrufen
    def get_produkt(self, name):
        """
        Retrieve a product by its name.

        :param name: The name of the product to retrieve.
        :return: The Produkt instance if found, else None.
        """
        return self.produkte.get(name)

    # 2.4 String-Darstellung des Bestands
    def __str__(self):
        """
        Return a readable representation of the current stock.

        :return: A string showing all products and their quantities.
        """
        output = "Bestand:\n"
        for produkt in self.produkte.values():
            output += f"{produkt.name}: {produkt.menge} Stück\n"
        return output

    # 2.5 Produkte aus einer CSV-Datei importieren
    def import_from_csv(self, filename):
        """
        Import products from a CSV file into the stock.

        :param filename: The name of the CSV file to import from.
        """
        filepath = os.path.join('CSV', filename)
        with open(filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name, menge = row
                produkt = Produkt(name, int(menge))
                self.add_produkt(produkt)

    # 2.6 Aktuellen Bestand in eine CSV-Datei exportieren
    def export_to_csv(self, filename):
        """
        Export the current stock to a CSV file.

        :param filename: The name of the CSV file to export to.
        """
        filepath = os.path.join('CSV', filename)
        with open(filepath, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for produkt in self.produkte.values():
                writer.writerow([produkt.name, produkt.menge])