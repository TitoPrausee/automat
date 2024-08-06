"""
Stock
======

"""
import csv  # Importiert das Modul zum Arbeiten mit CSV-Dateien
import os   # Importiert das Modul zum Arbeiten mit Betriebssystem-Funktionen

class Produkt:
    """Repräsentiert ein einzelnes Produkt mit Name, Preis und Menge."""
    def __init__(self, name, preis, menge):
        self.name = name  # Name des Produkts
        self.preis = preis  # Preis des Produkts
        self.menge = menge  # Menge des Produkts

class Bestand:
    """Verwaltet eine Sammlung von Produkten."""
    def __init__(self):
        self.produkte = {}  # Wörterbuch zur Speicherung der Produkte

    def add_produkt(self, produkt):
        """Fügt ein Produkt zum Bestand hinzu.
        Wenn das Produkt bereits existiert, wird die Menge erhöht."""
        if produkt.name in self.produkte:
            self.produkte[produkt.name].menge += produkt.menge
        else:
            self.produkte[produkt.name] = produkt

    def remove_produkt(self, name, menge):
        """Entfernt eine bestimmte Menge eines Produkts aus dem Bestand."""
        if name in self.produkte:
            if self.produkte[name].menge >= menge:
                self.produkte[name].menge -= menge
            else:
                print("Nicht genug Produkte auf Lager.")
        else:
            print("Produkt nicht gefunden.")

    def get_produkt(self, name):
        """Gibt ein Produkt anhand seines Namens zurück."""
        return self.produkte.get(name)

    def __str__(self):
        """Gibt eine lesbare Darstellung des Bestands zurück."""
        output = "Bestand:\n"
        for produkt in self.produkte.values():
            output += f"{produkt.name}: {produkt.menge} Stück\n"
        return output

    def import_from_csv(self, filename):
        """Importiert Produkte aus einer CSV-Datei."""
        filepath = os.path.join('CSV', filename)
        with open(filepath, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name, preis, menge = row
                produkt = Produkt(name, float(preis), int(menge))
                self.add_produkt(produkt)

    def export_to_csv(self, filename):
        """Exportiert den Bestand in eine CSV-Datei."""
        filepath = os.path.join('CSV', filename)
        with open(filepath, 'w') as csvfile:
            writer = csv.writer(csvfile)
            for produkt in self.produkte.values():
                writer.writerow([produkt.name, produkt.preis, produkt.menge])
