# 1. Klasse zur Preiskalkulation
class PriceCalculator:
    """
    PriceCalculator is responsible for handling the prices of products
    and retrieving the price of a specific product.

    Methods:
        get_price(drink): Returns the price of the given drink.
    """

    # 1.1 Konstruktor der Klasse
    def __init__(self, csv_handler, file_path):
        """
        Initializes the PriceCalculator with the CSV handler and the file path.

        :param csv_handler: Instance of CSVHandler for reading CSV data.
        :param file_path: Path to the CSV file containing price data.
        """
        self.csv_handler = csv_handler  # Handler for CSV operations
        self.file_path = file_path  # Path to the CSV file
        self.prices_data = self.csv_handler.read_csv(self.file_path)  # Load price data from CSV

    # 1.2 Preis eines bestimmten Produkts abrufen
    def get_price(self, drink):
        """
        Returns the price of the given drink.

        :param drink: The name of the drink to retrieve the price for.
        :return: The price of the drink, or 0 if not found.
        """
        return self.prices_data.get(drink, 0)
