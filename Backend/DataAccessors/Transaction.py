import csv  # Modul zum Arbeiten mit CSV-Dateien
import os   # Modul zum Arbeiten mit Betriebssystemfunktionen

# 1. Klasse zur Verwaltung von Transaktionsdaten
class Transaction:
    """
    Handles the saving of transaction data to a CSV file.

    Attributes:
        dirname: Directory path to the location of the CSV file.
        csvPath: Full path to the transactions CSV file.
    """

    # 1.1 Statische Attribute für Pfade
    dirname = os.path.dirname(os.path.dirname(__file__))  # Verzeichnisname für das CSV-Verzeichnis
    csvPath = os.path.join(dirname, 'CSV/transactions.csv')  # Vollständiger Pfad zur CSV-Datei

    # 1.2 Methode zum Speichern einer Transaktion
    @staticmethod
    def Save(item):
        """
        Save the transaction data to the CSV file.

        :param item: The item to be saved in the transaction log.
        """
        with open(Transaction.csvPath, 'a', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, ['item'])  # CSV-Schreiber mit 'item' als Spaltenname
            writer.writerow({'item': item})  # Schreibe das übergebene Item in die CSV-Datei
