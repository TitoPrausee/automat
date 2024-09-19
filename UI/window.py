import tkinter as tk
from tkinter import Button, Label, DISABLED, simpledialog, messagebox, Frame
from math import ceil, floor
import csv
import os
from UI.admin_panel import AdminPanel
from datetime import datetime
from Backend.DataAccessors.Stock import Stock
from Backend.CSVHandler import CSVHandler
from Backend.Tools.PriceCalculator import PriceCalculator  # Import PriceCalculator
from UI.admin_panel import AdminPanel  # Import AdminPanel

# Globale Variablen initialisieren
global enteredSum, sumToEnter, change, transaction_id, guthaben
global labelEnteredSum, labelSumToEnter, labelChange, guthabenLabel
global drinksFrame
guthaben = 0
enteredSum = 0
sumToEnter = 0
change = 0
transaction_id = 1

def create_UI(root, price_calculator):
    global guthabenLabel
    global drinksFrame

    root.grid_columnconfigure(0, weight=1)  # Column 0
    root.grid_columnconfigure(1, weight=1)  # Column 1 (centered labels will be here)
    root.grid_columnconfigure(2, weight=1)  # Column 2
    
    Label(root, text="Getränkeautomat", font=("Arial", 22)).grid(row=0, column=1, sticky="NSEW", padx=10)

    guthabenLabel = Label(root,text="Guthaben: " + guthaben.__str__(),font=("Arial", 20))
    guthabenLabel.grid(row=1, column=1, pady=30, sticky="NESW")

    moneyFrame = tk.Frame(root, bg="white", borderwidth=2, relief="sunken", height=250)
    moneyFrame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)
    moneyFrame.grid_columnconfigure(0, weight=1)
    moneyFrame.grid_columnconfigure(1, weight=1)
    moneyFrame.grid_columnconfigure(2, weight=1)

    # Geld-Eingabe Buttons für Münzen
    coin_values = [0.5, 1, 2]
    for i, coin in enumerate(coin_values):
        Button(moneyFrame, highlightbackground="white", text=f"{coin}€", command=lambda value=coin: enter_money(value)).grid(row=0, column=i, sticky="we")

    # Geld-Eingabe Buttons für Scheine
    bill_values = [10, 5, 20]
    for i, bill in enumerate(bill_values):
        Button(moneyFrame, highlightbackground="white", width=8, text=f"{bill}€", command=lambda value=bill: enter_money(value)).grid(row=1, column=i, sticky="we")


    drinksFrame = tk.Frame(root, bg="white", borderwidth=2, relief="sunken", height=250)
    drinksFrame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)
    drinksFrame.grid_columnconfigure(0, weight=1)
    drinksFrame.grid_columnconfigure(1, weight=1)
    drinksFrame.grid_columnconfigure(2, weight=1)
    #drinks should be added here
    gernerate_drink_buttons(["Cola", "Fanta", "Sprite", "Wasser"])

    Button(root, text="Ausgabe", state=DISABLED).grid(row=4, column=1, sticky="ns", pady=10)
    # Button(root, text="Abbruch", command=reset_money).grid(row=4, column=0)
    # Button(root, text="Wartung").grid(row=4, column=3)

def gernerate_drink_buttons(drinks):
    drinksperrow = 3
    global drinksFrame
    for i, drink in enumerate(drinks):
        currentColumn = i % drinksperrow
        currentRow = floor(i / drinksperrow)
        if currentColumn < 0:
            currentColumn = 0
        Button(drinksFrame, text=drink, highlightbackground="white", width=7).grid(column=currentColumn, row=currentRow, sticky="ew")

def enter_money(value):
    global guthabenLabel, guthaben
    guthaben = guthaben + value
    guthabenLabel.config(text=f"Guhaben: {guthaben}")

def reset_money():
    global guthabenLabel, guthaben
    guthaben = 0
    guthabenLabel.config(text="Guhaben: 0")

#---------------------------------------------
#ignore everything below
#---------------------------------------------

# Global variables for labels
labelEnteredSum = None
labelSumToEnter = None
labelChange = None

def create_window(root, price_calculator):
    """
    This function creates the main window of the application and initializes the UI components.
    It also sets up dynamic updates for product buttons and stock levels.
    
    :param root: The Tkinter root window (main window).
    :param price_calculator: Instance of the PriceCalculator class for handling product prices.
    """
    global enteredSum, sumToEnter, change, transaction_id
    global labelEnteredSum, labelSumToEnter, labelChange

    # Initialize the CSV handler and load stock data from the CSV file
    csv_handler = CSVHandler()  # Create an instance of CSVHandler
    stock_file_path = os.path.join(os.path.dirname(__file__), '..', 'Backend', 'CSV', 'stock.csv')
    stock_manager = Stock(csv_handler, stock_file_path)  # Create an instance of Stock class

    # Method to update the UI dynamically
    def update_ui():
        """
        This function is called to dynamically update the UI when stock or prices change.
        It clears all existing widgets and rebuilds the UI from scratch.
        """
        # Remove all existing widgets from the window
        for widget in root.winfo_children():
            widget.destroy()
        # Rebuild the UI
        build_ui()

    # Function to build the UI and display products and their quantities
    def build_ui():
        """
        Builds the UI by creating buttons for each product based on the stock and price data.
        Buttons are only enabled if the product is in stock.
        """
        drinks = price_calculator.prices_data  # Prices from prices.csv
        stock = stock_manager.stock_data  # Stock data from stock.csv

        drinksCountInRow = 3
        drinksRowsCount = ceil(len(drinks) / drinksCountInRow)

        # Dynamically generate buttons for each product based on stock and price
        for idx, (drink, price) in enumerate(drinks.items()):
            buttonRow = idx // drinksCountInRow
            buttonColumn = idx % drinksCountInRow
            quantity = stock.get(drink, 0)  # Get the product quantity from stock.csv

            # Button text showing product name, price, and quantity
            buttonText = f"{drink} - {price:.2f}€ (Quantity: {quantity})"

            # Enable the button if the product is in stock, otherwise disable it
            if stock_manager.is_in_stock(drink, 1):
                button = Button(root, text=buttonText, command=lambda drink=drink, price=price: add_drink(drink, price, stock_manager, update_ui))
            else:
                button = Button(root, text=f"{drink} - SOLD OUT", state=DISABLED)

            button.grid(row=buttonRow, column=buttonColumn)

        # Labels to display entered amount, amount still to be paid, and change
        global labelEnteredSum, labelSumToEnter, labelChange
        labelEnteredSum = Label(root, text="Entered: 0")
        labelEnteredSum.grid(row=drinksRowsCount + 1, column=0)
        labelSumToEnter = Label(root, text="Still to enter: 0")
        labelSumToEnter.grid(row=drinksRowsCount + 2, column=0)
        labelChange = Label(root, text="Change: 0")
        labelChange.grid(row=drinksRowsCount + 3, column=0)

        # Buttons for entering coins
        coin_values = [0.5, 1, 2]
        for i, coin in enumerate(coin_values):
            Button(root, text=f"{coin}€", command=lambda value=coin: enter_sum(value)).grid(row=drinksRowsCount + 4, column=i)

        # Buttons for entering bills
        bill_values = [10, 20]
        for i, bill in enumerate(bill_values):
            Button(root, text=f"{bill}€", command=lambda value=bill: enter_sum(value)).grid(row=drinksRowsCount + 5, column=i)

        Button(root, text="Finish", command=reset).grid(row=drinksRowsCount + 6, column=0)

        # Button for admin access to restock products
        Button(root, text="Restock", command=open_admin_panel).grid(row=drinksRowsCount + 7, column=0)

    # Open the admin panel and update the UI when a new product is added
    def open_admin_panel():
        """
        Opens the admin panel where new products can be added or stock can be updated.
        After changes, the UI is dynamically updated to reflect the new stock.
        """
        password = simpledialog.askstring("Enter Password", "Please enter the admin password:", show='*')
        if password == "123":  # Simple password check for demonstration (replace with secure method in production)
            # Open the admin panel
            admin_root = tk.Toplevel()
            admin_root.title("Admin Panel")

            # Create AdminPanel with price_calculator and stock_manager
            AdminPanel(admin_root, stock_manager, price_calculator, update_ui)  # Pass the update_ui callback to dynamically update the UI
            admin_root.mainloop()
        else:
            messagebox.showerror("Error", "Incorrect password!")

    # Build the UI when the window is first created
    build_ui()

# Function to handle the purchase of a drink
def add_drink(drink, price, stock_manager, update_ui_callback):
    """
    Handles the logic when a product is purchased. Updates the stock, recalculates the totals,
    and dynamically updates the UI to reflect the new stock.

    :param drink: The name of the product being purchased.
    :param price: The price of the product.
    :param stock_manager: The stock manager instance to update the stock.
    :param update_ui_callback: The callback function to update the UI after the purchase.
    """
    global sumToEnter
    sumToEnter += price

    # Decrease the stock by 1
    stock_manager.update_stock(drink, 1)  # Use the 'update_stock' method of the 'Stock' class

    update_labels()
    log_transaction(drink, 1, price, price)  # Log the transaction (1 item per click)

    # Dynamically update the UI to show the reduced stock
    update_ui_callback()

# Function to update the labels for entered sum, remaining sum, and change
def update_labels():
    """
    Updates the labels that show the entered amount, the amount still to be paid,
    and the change to be returned.
    """
    global enteredSum, sumToEnter, change
    global labelEnteredSum, labelSumToEnter, labelChange
    
    change = enteredSum - sumToEnter if enteredSum >= sumToEnter else 0
    labelEnteredSum.config(text=f"Entered: {enteredSum}")
    labelSumToEnter.config(text=f"Still to enter: {max(sumToEnter - enteredSum, 0)}")
    labelChange.config(text=f"Change: {change}")

# Function to handle the sum entered by the user
def enter_sum(value):
    """
    Adds the entered amount to the total and updates the labels.

    :param value: The value of the coin or bill entered.
    """
    global enteredSum
    enteredSum += value
    update_labels()

# Function to reset all values (used when a transaction is completed)
def reset():
    """
    Resets all values (entered sum, total sum to enter, and change) to 0.
    Updates the labels to reflect the reset values.
    """
    global sumToEnter, enteredSum, change
    sumToEnter = 0
    enteredSum = 0
    change = 0
    update_labels()

# Function to log the transaction to a CSV file
def log_transaction(item, quantity, price, total):
    """
    Logs a transaction to the transactions.csv file.

    :param item: The product name.
    :param quantity: The quantity purchased.
    :param price: The price of the product.
    :param total: The total price of the transaction.
    """
    global transaction_id
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transaction_data = [transaction_id, item, quantity, price, total, timestamp]
    
    # Write the transaction data to the CSV file
    with open(os.path.join(os.path.dirname(__file__), '..', 'Backend', 'CSV', 'transactions.csv'), mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(transaction_data)

    transaction_id += 1