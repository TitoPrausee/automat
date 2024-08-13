import os
import tkinter as tk
from Backend.CSVHandler import CSVHandler
from Backend.Tools.PriceCalculator import PriceCalculator
from Backend.DataAccessors.Stock import Stock
from UI import window

def main():
    csv_handler = CSVHandler()
    
    # Korrekte Pfade für die CSV-Dateien
    prices_csv_path = os.path.join(os.path.dirname(__file__), 'Backend', 'CSV', 'prices.csv')
    stock_csv_path = os.path.join(os.path.dirname(__file__), 'Backend', 'CSV', 'stock.csv')

    price_calculator = PriceCalculator(csv_handler, prices_csv_path)
    stock_manager = Stock(csv_handler, stock_csv_path)

    root = tk.Tk()
    root.title("Automat")
    root.geometry('700x1000')

    window.create_window(root, price_calculator, stock_manager)  # Initialisiere die UI

    root.mainloop()

if __name__ == "__main__":
    main()
