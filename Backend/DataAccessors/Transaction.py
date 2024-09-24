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
        Liest die CSV-Datei und gibt die nächste verfügbare transaction_id zurück.
        Falls keine Transaktionen vorhanden sind, wird die transaction_id auf 1 gesetzt.

        :return: Die nächste transaction_id (int)
        """
        # Standardmäßige transaction_id, falls keine Daten vorhanden sind
        next_transaction_id = 1

        # Überprüfen, ob die CSV-Datei existiert und Daten enthält
        if os.path.exists(Transaction.csvPath):
            with open(Transaction.csvPath, 'r') as csvFile:
                reader = csv.DictReader(csvFile)
                # Durchlaufen der Zeilen, um die höchste transaction_id zu finden
                for row in reader:
                    try:
                        # Überprüfen, ob 'transaction_id' in der Zeile existiert
                        current_id = int(row['transaction_id'])
                        next_transaction_id = max(
                            next_transaction_id, current_id + 1)
                    except (ValueError, KeyError):
                        # Bei ungültigen oder fehlenden Werten einfach überspringen
                        continue

        return next_transaction_id
