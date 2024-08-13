class PriceCalculator:
    def __init__(self, csv_handler, file_path):
        self.csv_handler = csv_handler
        self.file_path = file_path
        self.prices_data = self.csv_handler.read_csv(self.file_path)

    def get_price(self, drink):
        return self.prices_data.get(drink, 0)
