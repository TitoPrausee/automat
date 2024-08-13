import csv  # Modul zum Arbeiten mit CSV-Dateien
import os   # Modul zum Arbeiten mit Betriebssystemfunktionen

# 1. Klasse zur Verwaltung von Preisdaten
class Price:
    """
    Handles reading and updating prices from and to a CSV file.

    Attributes:
        _dirname: Directory path to the location of the CSV file.
        _csvPath: Full path to the prices CSV file.
    """

    # 1.1 Statische Attribute für Pfade
    _dirname = os.path.dirname(os.path.dirname(__file__))  # Verzeichnisname für das CSV-Verzeichnis
    _csvPath = os.path.join(_dirname, 'CSV/price.csv')  # Vollständiger Pfad zur CSV-Datei

    # 1.2 Methode zum Lesen aller Preise aus der CSV-Datei
    @staticmethod
    def readAllPrices():
        """
        Reads all prices from the CSV file and returns them as a dictionary.

        :return: A dictionary with product names as keys and prices as values.
        """
        pricesData = {}
        with open(Price._csvPath, "r", newline='') as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                pricesData[row['name']] = float(row['price'])  # Preis als Float speichern

        return pricesData

    # 1.3 Methode zum Aktualisieren eines Preises in der CSV-Datei
    @staticmethod
    def updatePrice(name, price):
        """
        Updates the price of a specific product in the CSV file.

        :param name: The name of the product to update.
        :param price: The new price of the product.
        """
        if not os.path.isfile(Price._csvPath):  # Überprüfen, ob die CSV-Datei existiert
            return

        # Alle Daten aus der CSV-Datei lesen
        with open(Price._csvPath, "r", newline='') as csvFile:
            reader = csv.DictReader(csvFile)
            priceData = list(reader)

        priceDict = {item['name']: float(item['price']) for item in priceData}

        # Preis für das angegebene Produkt aktualisieren
        if name in priceDict:
            priceDict[name] = price

        updatedPriceData = [{'name': name, 'price': price} for name, price in priceDict.items()]

        # Aktualisierte Daten in die CSV-Datei speichern
        with open(Price._csvPath, "w", newline='') as csvFile:
            fieldnames = ['name', 'price']
            writer = csv.DictWriter(csvFile, fieldnames)
            writer.writeheader()
            for item in updatedPriceData:
                writer.writerow(item)
