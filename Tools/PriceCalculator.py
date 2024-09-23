# 1. Klasse zur Preiskalkulation
class PriceCalculator:
    """
    Die Klasse PriceCalculator ist für die Verwaltung der Produktpreise und
    das Abrufen des Preises eines bestimmten Produkts zuständig.

    Methoden:
        get_price(drink): Gibt den Preis des angegebenen Getränks zurück.
    """

    # 1.1 Konstruktor der Klasse
    def __init__(self, csv_handler, file_path):
        """
        Initialisiert den PriceCalculator mit dem CSV-Handler und dem Dateipfad.

        :param csv_handler: Instanz von CSVHandler zum Lesen von CSV-Daten.
        :param file_path: Pfad zur CSV-Datei mit den Preisdaten.
        """
        self.csv_handler = csv_handler  # Handler für CSV-Operationen
        self.file_path = file_path  # Pfad zur CSV-Datei
        self.prices_data = self.csv_handler.read_csv(self.file_path)  # Preisdaten aus CSV laden

    # 1.2 Preis eines bestimmten Produkts abrufen
    def get_price(self, drink):
        """
        Gibt den Preis des angegebenen Getränks zurück.

        :param drink: Der Name des Getränks, dessen Preis abgerufen werden soll.
        :return: Der Preis des Getränks oder 0, falls nicht gefunden.
        """
        return self.prices_data.get(drink, 0)