import csv

# 1. Klasse zur Handhabung von CSV-Dateien
class CSVHandler:
    
    # 1.1 Konstruktor der Klasse
    def __init__(self):
        pass

    # 1.2 Funktion zum Lesen von CSV-Dateien
    def read_csv(self, file_path):
        data = {}
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'price' in row:
                    # Wenn 'price' vorhanden ist, als float speichern
                    data[row['name']] = float(row['price'])
                elif 'quantity' in row:
                    # Wenn 'quantity' vorhanden ist, als int speichern
                    data[row['name']] = int(row['quantity'])
        return data

    # 1.3 Funktion zum Schreiben von Daten in CSV-Dateien
    def write_csv(self, file_path, data):
        with open(file_path, mode='w', newline='') as file:
            if 'price' in data:
                # CSV-Datei für Preise erstellen
                writer = csv.DictWriter(file, fieldnames=['name', 'price'])
                writer.writeheader()
                for name, price in data.items():
                    writer.writerow({'name': name, 'price': price})
            else:
                # CSV-Datei für Bestände erstellen
                writer = csv.DictWriter(file, fieldnames=['name', 'quantity'])
                writer.writeheader()
                for name, quantity in data.items():
                    writer.writerow({'name': name, 'quantity': quantity})
