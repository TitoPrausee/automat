class Stock:
    def __init__(self, csv_handler, file_path):
        self.csv_handler = csv_handler
        self.file_path = file_path
        self.stock_data = self.csv_handler.read_csv(self.file_path)

    def is_in_stock(self, drink, quantity=1):
        return self.stock_data.get(drink, 0) >= quantity

    def update_stock(self, drink, quantity):
        if self.is_in_stock(drink, quantity):
            self.stock_data[drink] -= quantity
            self.csv_handler.write_csv(self.file_path, self.stock_data)
