# 1. Klasse zur Verwaltung des Lagerbestands
class Stock:
    """
    Stock is responsible for managing the inventory of products, including
    checking stock levels and updating stock quantities.

    Methods:
        is_in_stock(drink, quantity=1): Checks if the specified quantity of a product is in stock.
        update_stock(drink, quantity): Updates the stock by reducing the quantity of a product.
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
        self.stock_data = self.csv_handler.read_csv(self.file_path)  # Load stock data from CSV

    # 1.2 Überprüfen, ob ein Produkt in ausreichender Menge auf Lager ist
    def is_in_stock(self, drink, quantity=1):
        """
        Checks if the specified quantity of a product is in stock.

        :param drink: The name of the drink to check.
        :param quantity: The quantity to check for, defaults to 1.
        :return: True if the stock is sufficient, False otherwise.
        """
        return self.stock_data.get(drink, 0) >= quantity

    # 1.3 Bestand aktualisieren
    def update_stock(self, drink, quantity):
        """
        Updates the stock by reducing the quantity of a product.

        :param drink: The name of the drink to update.
        :param quantity: The quantity to reduce from the stock.
        """
        if self.is_in_stock(drink, quantity):
            self.stock_data[drink] -= quantity  # Reduce the stock quantity
            self.csv_handler.write_csv(self.file_path, self.stock_data)  # Save the updated stock to CSV
