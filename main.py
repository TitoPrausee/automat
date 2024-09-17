import os
import tkinter as tk
from Backend.CSVHandler import CSVHandler
from Backend.Tools.PriceCalculator import PriceCalculator
from UI import window  # Korrektur: Du brauchst Stock hier nicht zu importieren

# 1. Hauptfunktion für den Start der Anwendung
def main():
    # 1.1 CSV-Handler initialisieren
    csv_handler = CSVHandler()
    
    # 1.2 Korrekte Pfade für die CSV-Dateien festlegen
    prices_csv_path = os.path.join(os.path.dirname(__file__), 'Backend', 'CSV', 'prices.csv')

    # 1.3 Preisrechner initialisieren
    price_calculator = PriceCalculator(csv_handler, prices_csv_path)

    # 1.4 Hauptfenster erstellen
    root = tk.Tk()
    root.title("Automat")
    root.geometry('700x1000')

    # 1.5 UI initialisieren (nur root und price_calculator übergeben)
    window.create_window(root, price_calculator)

    # 1.6 Haupt-Event-Loop starten
    root.mainloop()

# 2. Programmstart prüfen
if __name__ == "__main__":
    main()