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
    # Verzeichnisname für das CSV-Verzeichnis
    dirname = os.path.dirname(os.path.dirname(__file__))
    # Vollständiger Pfad zur CSV-Datei
    csvPath = os.path.join(dirname, 'CSV/transactions.csv')

    # 1.2 Methode zum Speichern einer Transaktion
    @staticmethod
    def Save(data):
        """
        Speichert die Transaktionsdaten in der CSV-Datei.

        :param item: Der Artikel, der im Transaktionsprotokoll gespeichert werden soll.
        """
        data['transaction_id'] = Transaction.get_next_transaction_id()

        if os.path.exists(Transaction.csvPath):
            # Öffnen der CSV-Datei im Anhängemodus ('a'), um neue Transaktionen hinzuzufügen
            with open(Transaction.csvPath, 'a') as csvFile:
                # Erstellen eines DictWriters, um eine Zeile mit der Spalte 'item' zu schreiben
                # CSV-Writer mit 'item' als Spaltenname
                writer = csv.DictWriter(
                    csvFile, ['transaction_id', 'item', 'quantity', 'price', 'total', 'timestamp'])
                # Schreiben des Artikels in die CSV-Datei
                # Schreiben des übergebenen Artikels in die CSV-Datei
                writer.writerow(data)

    # 1.3 Methode zum Abrufen der nächsten transaction_id
    @staticmethod
    def get_next_transaction_id():
        """
        Liest die letzte Zeile der CSV-Datei und gibt die nächste verfügbare transaction_id zurück.
        Falls keine Transaktionen vorhanden sind, wird die transaction_id auf 1 gesetzt.

        :return: Die nächste transaction_id (int)
        """
        next_transaction_id = 1

        # Überprüfen, ob die CSV-Datei existiert und nicht leer ist
        if os.path.exists(Transaction.csvPath):
            with open(Transaction.csvPath, 'r') as csvFile:
                reader = list(csv.DictReader(csvFile))
                if reader:
                    # Letzte Zeile nehmen und transaction_id um 1 erhöhen
                    last_transaction = reader[-1]
                    try:
                        next_transaction_id = int(
                            last_transaction['transaction_id']) + 1
                    except (ValueError, KeyError):
                        pass  # Falls die transaction_id ungültig ist, behalten wir den Standardwert 1

        return next_transaction_id