import os
import tkinter as tk
from Backend.CSVHandler import CSVHandler
from Backend.Tools.PriceCalculator import PriceCalculator
from Backend.DataAccessors.Stock import Stock
from UI import window

# 1. Hauptfunktion für den Start der Anwendung
def main():
    # 1.1 CSV-Handler initialisieren
    csv_handler = CSVHandler()
    
    # 1.2 Korrekte Pfade für die CSV-Dateien festlegen
    prices_csv_path = os.path.join(os.path.dirname(__file__), 'Backend', 'CSV', 'prices.csv')
    stock_csv_path = os.path.join(os.path.dirname(__file__), 'Backend', 'CSV', 'stock.csv')

    # 1.3 Preisrechner und Lagerverwaltung initialisieren
    price_calculator = PriceCalculator(csv_handler, prices_csv_path)
    stock_manager = Stock(csv_handler, stock_csv_path)

    # 1.4 Hauptfenster erstellen
    root = tk.Tk()
    root.title("Automat")
    root.geometry('600x800')
    root.minsize(width=600, height=800)
    root.maxsize(width=600, height=800)

    # 1.5 UI initialisieren
    # window.create_window(root, price_calculator, stock_manager)
    window.create_UI(root, price_calculator, stock_manager)

    # 1.6 Haupt-Event-Loop starten
    root.mainloop()

# 2. Programmstart prüfen
if __name__ == "__main__":
    main()
