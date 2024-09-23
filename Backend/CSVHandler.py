# CSVHandler.py

import csv

class CSVHandler:
    """
    Eine Klasse zum Lesen und Schreiben von Daten in CSV-Dateien.

    Methoden:
        read_csv(file_path): Liest Daten aus einer CSV-Datei und gibt sie als Dictionary zurück.
        write_csv(file_path, data): Schreibt Daten aus einem Dictionary in eine CSV-Datei.
    """

    def read_csv(self, file_path):
        """
        Liest Daten aus einer CSV-Datei und gibt sie als Dictionary zurück.

        :param file_path: Der Pfad zur CSV-Datei.
        :return: Ein Dictionary, das die Daten aus der CSV-Datei enthält.
                 Die Schlüssel des Dictionaries entsprechen den Spaltenüberschriften in der CSV-Datei.
        """
        data = {}  # Initialisieren eines leeren Dictionaries zum Speichern der Daten
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)  # Erstellen eines DictReader-Objekts zum Lesen der CSV-Datei
            for row in reader:  # Iterieren über jede Zeile in der CSV-Datei
                if 'price' in row:  # Wenn die Zeile eine 'price'-Spalte enthält
                    data[row['name']] = float(row['price'])  # Füge den Preis als Float zum Dictionary hinzu
                elif 'quantity' in row:  # Wenn die Zeile eine 'quantity'-Spalte enthält
                    data[row['name']] = int(row['quantity'])  # Füge die Menge als Integer zum Dictionary hinzu
        return data  # Gib das Dictionary mit den Daten zurück

    def write_csv(self, file_path, data):
        """
        Schreibt Daten aus einem Dictionary in eine CSV-Datei.

        :param file_path: Der Pfad zur CSV-Datei.
        :param data: Ein Dictionary, das die zu schreibenden Daten enthält.
        """
        with open(file_path, mode='w', newline='') as file:
            # Wenn alle Werte im Dictionary Floats sind, schreibe die Daten mit den Spaltenüberschriften 'name' und 'price'
            if all(isinstance(value, float) for value in data.values()):
                writer = csv.DictWriter(file, fieldnames=['name', 'price'])
                writer.writeheader()  # Schreibe die Spaltenüberschriften in die CSV-Datei
                for name, price in data.items():  # Iteriere über die Daten und schreibe jede Zeile
                    writer.writerow({'name': name, 'price': price})
            # Andernfalls schreibe die Daten mit den Spaltenüberschriften 'name' und 'quantity'
            else:
                writer = csv.DictWriter(file, fieldnames=['name', 'quantity'])
                writer.writeheader()  # Schreibe die Spaltenüberschriften in die CSV-Datei
                for name, quantity in data.items():  # Iteriere über die Daten und schreibe jede Zeile
                    writer.writerow({'name': name, 'quantity': quantity})