import os
import tkinter as tk
from Backend.CSVHandler import CSVHandler
from Backend.Tools.PriceCalculator import PriceCalculator
from UI import window  # Corrected import: No need to import Stock here

# 1. Main function to start the application
def main():
    """
    This is the main function that initializes the necessary components
    and starts the graphical user interface (GUI) for the vending machine application.
    """
    
    # 1.1 Initialize the CSV handler to manage CSV file operations
    csv_handler = CSVHandler()
    
    # 1.2 Set the correct paths for the CSV files (prices.csv and stock.csv)
    prices_csv_path = os.path.join(os.path.dirname(__file__), 'Backend', 'CSV', 'prices.csv')

    # 1.3 Initialize the price calculator with the CSV handler and the path to prices.csv
    price_calculator = PriceCalculator(csv_handler, prices_csv_path)

    # 1.4 Create the main window (root window) where the application UI will be rendered
    root = tk.Tk()
    root.title("Automat")  # Set the window title
    root.geometry('700x1000')  # Set the window size (width x height)
    root.maxsize(width=700 , height=400)
    root.minsize(width=700 , height=400)

    # 1.5 Initialize the UI by calling the create_window function from window.py
    # Only pass root (the main window) and price_calculator (for handling prices)
    window.create_window(root, price_calculator)

    # 1.6 Start the main event loop (Tkinter's main loop for handling events)
    root.mainloop()

# 2. Check if the script is being executed directly (and not imported as a module)
if __name__ == "__main__":
    main()