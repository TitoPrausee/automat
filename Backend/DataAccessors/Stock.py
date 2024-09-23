# 1. Klasse zur Verwaltung des Lagerbestands
class Stock:
    """
    Die Klasse Stock ist für die Verwaltung des Produktinventars zuständig,
    einschließlich der Überprüfung des Lagerbestands und der Aktualisierung
    von Lagermengen.

    Methoden:
        is_in_stock(drink, quantity=1): Überprüft, ob die angegebene Menge
        eines Produkts auf Lager ist.
        update_stock(drink, quantity): Aktualisiert den Lagerbestand, indem
        die Menge eines Produkts reduziert wird.
        add_stock(drink, quantity): Fügt dem Lagerbestand eines Produkts
        eine bestimmte Menge hinzu.
        save_stock(): Speichert die aktuellen Lagerbestandsdaten in der CSV-Datei.
        load_stock(): Lädt Lagerbestandsdaten aus der CSV-Datei.
    """

    # 1.1 Konstruktor der Klasse
    def __init__(self, csv_handler, file_path):
        """
        Initialisiert die Klasse Stock mit dem CSV-Handler und dem Dateipfad.

        :param csv_handler: Instanz von CSVHandler zum Lesen und Schreiben von CSV-Daten.
        :param file_path: Pfad zur CSV-Datei mit den Lagerbestandsdaten.
        """
        self.csv_handler = csv_handler  # Handler für CSV-Operationen
        self.file_path = file_path  # Pfad zur CSV-Datei
        self.stock_data = self.load_stock()  # Lagerbestandsdaten aus CSV laden

    # 1.2 Überprüfen, ob ein Produkt in ausreichender Menge auf Lager ist
    def is_in_stock(self, drink, quantity=1):
        """
        Überprüft, ob die angegebene Menge eines Produkts auf Lager ist.

        :param drink: Der Name des zu überprüfenden Getränks.
        :param quantity: Die zu überprüfende Menge, Standard ist 1.
        :return: True, wenn der Lagerbestand ausreichend ist, sonst False.
        """
        return self.stock_data.get(drink, 0) >= quantity

    # 1.3 Bestand aktualisieren (Menge reduzieren)
    def update_stock(self, drink, quantity):
        """
        Aktualisiert den Lagerbestand, indem die Menge eines Produkts reduziert wird.

        :param drink: Der Name des zu aktualisierenden Getränks.
        :param quantity: Die Menge, die vom Lagerbestand abgezogen werden soll.
        """
        if self.is_in_stock(drink, quantity):
            self.stock_data[drink] -= quantity  # Reduzierung der Lagermenge
            self.save_stock()  # Speichern des aktualisierten Lagerbestands in CSV

    # 1.4 Bestand hinzufügen (Menge erhöhen)
    def add_stock(self, drink, quantity):
        """
        Fügt dem Lagerbestand eines Produkts eine bestimmte Menge hinzu.

        :param drink: Der Name des zu aktualisierenden Getränks.
        :param quantity: Die Menge, die dem Lagerbestand hinzugefügt werden soll.
        """
        if drink in self.stock_data:
            self.stock_data[drink] += quantity  # Erhöhung der Lagermenge
        else:
            self.stock_data[drink] = quantity  # Neues Getränk mit der gegebenen Menge hinzufügen
        self.save_stock()  # Speichern des aktualisierten Lagerbestands in CSV

    # 1.5 Bestand speichern (CSV-Datei schreiben)
    def save_stock(self):
        """
        Speichert die aktuellen Lagerbestandsdaten in der CSV-Datei.
        """
        self.csv_handler.write_csv(self.file_path, self.stock_data)

    # 1.6 Bestand laden (CSV-Datei lesen)
    def load_stock(self):
        """
        Lädt Lagerbestandsdaten aus der CSV-Datei.

        :return: Ein Dictionary mit Produktnamen als Schlüssel und Mengen als Werte.
        """
        return self.csv_handler.read_csv(self.file_path)