# 1. Klasse zur Preiskalkulation
class PriceCalculator:
    """
    PriceCalculator ist für die Verwaltung der Preise von Produkten und
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
        # Handler für CSV-Operationen (z. B. Lesen der CSV-Datei)
        self.csv_handler = csv_handler  
        # Pfad zur CSV-Datei, die die Preisdaten enthält
        self.file_path = file_path  
        # Laden der Preisdaten aus der CSV-Datei in ein Dictionary
        self.prices_data = self.csv_handler.read_csv(self.file_path)  

    # 1.2 Preis eines bestimmten Produkts abrufen
    def get_price(self, drink):
        """
        Gibt den Preis des angegebenen Getränks zurück.

        :param drink: Der Name des Getränks, dessen Preis abgerufen werden soll.
        :return: Der Preis des Getränks oder 0, wenn es nicht gefunden wurde.
        """
        # Verwenden der get-Methode des Dictionaries, um den Preis abzurufen
        # Gibt 0 zurück, wenn das Getränk nicht gefunden wird (Standardwert)
        return self.prices_data.get(drink, 0)