import csv  # Modul für die Arbeit mit CSV-Dateien
import os   # Modul für die Arbeit mit Betriebssystemfunktionen

# 1. Klasse zur Verwaltung der Preisdaten
class Price:
    """
    Verwaltet das Lesen und Aktualisieren von Preisen aus und in eine CSV-Datei.

    Attribute:
        _dirname: Verzeichnispfad zum Speicherort der CSV-Datei.
        _csvPath: Vollständiger Pfad zur CSV-Datei mit den Preisen.
    """

    # 1.1 Statische Attribute für Pfade
    _dirname = os.path.dirname(os.path.dirname(__file__))  # Verzeichnisname für das CSV-Verzeichnis
    _csvPath = os.path.join(_dirname, 'CSV/price.csv')  # Vollständiger Pfad zur CSV-Datei

    # 1.2 Methode zum Lesen aller Preise aus der CSV-Datei
    @staticmethod
    def readAllPrices():
        """
        Liest alle Preise aus der CSV-Datei und gibt sie als Dictionary zurück.

        :return: Ein Dictionary mit Produktnamen als Schlüssel und Preisen als Werte.
        """
        pricesData = {}  # Dictionary zum Speichern von Produktnamen und deren Preisen
        with open(Price._csvPath, "r", newline='') as csvFile:
            reader = csv.DictReader(csvFile)
            # Iteration über jede Zeile und Speichern des Produktnamens und des Preises als Float
            for row in reader:
                pricesData[row['name']] = float(row['price'])  # Preis als Float speichern

        return pricesData  # Rückgabe des Dictionaries mit den Produktpreisen

    # 1.3 Methode zum Aktualisieren des Preises eines Produkts in der CSV-Datei
    @staticmethod
    def updatePrice(name, price):
        """
        Aktualisiert den Preis eines bestimmten Produkts in der CSV-Datei.

        :param name: Der Name des zu aktualisierenden Produkts.
        :param price: Der neue Preis des Produkts.
        """
        # Überprüfung, ob die CSV-Datei existiert
        if not os.path.isfile(Price._csvPath):
            return

        # Lesen aller Daten aus der CSV-Datei
        with open(Price._csvPath, "r", newline='') as csvFile:
            reader = csv.DictReader(csvFile)
            priceData = list(reader)  # Konvertieren des Reader-Objekts in eine Liste zur einfacheren Bearbeitung

        # Erstellen eines Dictionaries mit den aktuellen Preisen
        priceDict = {item['name']: float(item['price']) for item in priceData}

        # Aktualisieren des Preises für das angegebene Produkt
        if name in priceDict:
            priceDict[name] = price

        # Vorbereiten der aktualisierten Preisdaten für das Zurückschreiben in die CSV-Datei
        updatedPriceData = [{'name': name, 'price': price} for name, price in priceDict.items()]

        # Schreiben der aktualisierten Daten zurück in die CSV-Datei
        with open(Price._csvPath, "w", newline='') as csvFile:
            fieldnames = ['name', 'price']
            writer = csv.DictWriter(csvFile, fieldnames)
            writer.writeheader()  # Schreiben der Kopfzeile (Name, Preis)
            for item in updatedPriceData:
                writer.writerow(item)  # Schreiben des Namens und des aktualisierten Preises jedes Produkts