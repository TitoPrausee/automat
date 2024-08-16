# 1. Klasse zur Verwaltung des Lagerbestands
class Stock:
    """
    Stock is responsible for managing the inventory of products, including
    checking stock levels and updating stock quantities.

    Methods:
        is_in_stock(drink, quantity=1): Checks if the specified quantity of a product is in stock.
        update_stock(drink, quantity): Updates the stock by reducing the quantity of a product.
        add_stock(drink, quantity): Adds a specified quantity to the stock of a product.
        save_stock(): Saves the current stock data to the CSV file.
        load_stock(): Loads stock data from the CSV file.
    """

    # 1.1 Konstruktor der Klasse
    def __init__(self, csv_handler, file_path):
        """
        Initializes the Stock class with the CSV handler and the file path.

        :param csv_handler: Instance of CSVHandler for reading and writing CSV data.
        :param file_path: Path to the CSV file containing stock data.
        """
        self.csv_handler = csv_handler  # Handler for CSV operations
        self.file_path = file_path  # Path to the CSV file
        self.stock_data = self.load_stock()  # Load stock data from CSV

    # 1.2 Überprüfen, ob ein Produkt in ausreichender Menge auf Lager ist
    def is_in_stock(self, drink, quantity=1):
        """
        Checks if the specified quantity of a product is in stock.

        :param drink: The name of the drink to check.
        :param quantity: The quantity to check for, defaults to 1.
        :return: True if the stock is sufficient, False otherwise.
        """
        return self.stock_data.get(drink, 0) >= quantity

    # 1.3 Bestand aktualisieren (Menge reduzieren)
    def update_stock(self, drink, quantity):
        """
        Updates the stock by reducing the quantity of a product.

        :param drink: The name of the drink to update.
        :param quantity: The quantity to reduce from the stock.
        """
        if self.is_in_stock(drink, quantity):
            self.stock_data[drink] -= quantity  # Reduce the stock quantity
            self.save_stock()  # Save the updated stock to CSV

    # 1.4 Bestand hinzufügen (Menge erhöhen)
    def add_stock(self, drink, quantity):
        """
        Adds a specified quantity to the stock of a product.

        :param drink: The name of the drink to update.
        :param quantity: The quantity to add to the stock.
        """
        if drink in self.stock_data:
            self.stock_data[drink] += quantity  # Increase the stock quantity
        else:
            self.stock_data[drink] = quantity  # Add new drink with the given quantity
        self.save_stock()  # Save the updated stock to CSV

    # 1.5 Bestand speichern (CSV-Datei schreiben)
    def save_stock(self):
        """
        Saves the current stock data to the CSV file.
        """
        self.csv_handler.write_csv(self.file_path, self.stock_data)

    # 1.6 Bestand laden (CSV-Datei lesen)
    def load_stock(self):
        """
        Loads stock data from the CSV file.

        :return: A dictionary with product names as keys and quantities as values.
        """
        return self.csv_handler.read_csv(self.file_path)
