import csv  # Modul für die Arbeit mit CSV-Dateien
import os   # Modul für die Arbeit mit Betriebssystemfunktionen

# 1. Klasse zur Verwaltung der Transaktionsdaten
class Transaction:
    """
    Verwaltet das Speichern von Transaktionsdaten in einer CSV-Datei.

    Attribute:
        dirname: Verzeichnispfad zum Speicherort der CSV-Datei.
        csvPath: Vollständiger Pfad zur CSV-Datei mit den Transaktionen.
    """

    # 1.1 Statische Attribute für Pfade
    dirname = os.path.dirname(os.path.dirname(__file__))  # Verzeichnisname für das CSV-Verzeichnis
    csvPath = os.path.join(dirname, 'CSV/transactions.csv')  # Vollständiger Pfad zur CSV-Datei

    # 1.2 Methode zum Speichern einer Transaktion
    @staticmethod
    def Save(item):
        """
        Speichert die Transaktionsdaten in der CSV-Datei.

        :param item: Der Artikel, der im Transaktionsprotokoll gespeichert werden soll.
        """
        # Öffnen der CSV-Datei im Anhängemodus ('a'), um neue Transaktionen hinzuzufügen
        with open(Transaction.csvPath, 'a', newline='') as csvFile:
            # Erstellen eines DictWriters, um eine Zeile mit der Spalte 'item' zu schreiben
            writer = csv.DictWriter(csvFile, ['item'])  # CSV-Writer mit 'item' als Spaltenname
            # Schreiben des Artikels in die CSV-Datei
            writer.writerow({'item': item})  # Schreiben des übergebenen Artikels in die CSV-Datei