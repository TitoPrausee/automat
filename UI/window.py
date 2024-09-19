import tkinter as tk
from tkinter import Button, Label, DISABLED, simpledialog, messagebox
from math import ceil
import os
import csv
from datetime import datetime
from Backend.DataAccessors.Stock import Stock
from Backend.CSVHandler import CSVHandler
from Backend.Tools.PriceCalculator import PriceCalculator
from UI.admin_panel import AdminPanel

# Global variables initialization
global enteredSum, sumToEnter, change, transaction_id, guthaben
global guthabenLabel, drinksFrame
guthaben = 0
enteredSum = 0
sumToEnter = 0
change = 0
transaction_id = 1

# Global variables for labels
guthabenLabel = None


def create_window(root, price_calculator):
    global enteredSum, sumToEnter, change, transaction_id, guthaben
    global guthabenLabel

    csv_handler = CSVHandler()
    stock_file_path = os.path.join(os.path.dirname(
        __file__), '..', 'Backend', 'CSV', 'stock.csv')
    stock_manager = Stock(csv_handler, stock_file_path)

    def update_ui():
        # Clear all widgets and rebuild UI
        for widget in root.winfo_children():
            widget.destroy()
        build_ui()

    def build_ui():
        global guthabenLabel
        # Configure grid columns
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Create title label
        Label(root, text="Getränkeautomat", font=("Arial", 22)).grid(
            row=0, column=1, sticky="NSEW", padx=10)

        # Create balance label
        guthabenLabel = Label(root, text=f"Guthaben: {
                              guthaben:.2f}€", font=("Arial", 20))
        guthabenLabel.grid(row=1, column=1, pady=30, sticky="NESW")

        # Create frame for money buttons
        moneyFrame = tk.Frame(
            root, bg="white", borderwidth=2, relief="sunken", height=250)
        moneyFrame.grid(row=2, column=0, columnspan=3,
                        sticky="nsew", padx=20, pady=20)
        moneyFrame.grid_columnconfigure(0, weight=1)
        moneyFrame.grid_columnconfigure(1, weight=1)
        moneyFrame.grid_columnconfigure(2, weight=1)

        # Create coin buttons
        coin_values = [0.5, 1, 2]
        for i, coin in enumerate(coin_values):
            Button(moneyFrame, highlightbackground="white", width=8, text=f"{
                   coin}€", command=lambda value=coin: enter_money(value)).grid(row=0, column=i)

        # Create bill buttons
        bill_values = [10, 5, 20]
        for i, bill in enumerate(bill_values):
            Button(moneyFrame, highlightbackground="white", width=8, text=f"{
                   bill}€", command=lambda value=bill: enter_money(value)).grid(row=1, column=i)

        # Create frame for drink buttons
        drinksFrame = tk.Frame(
            root, bg="white", borderwidth=2, relief="sunken", height=250)
        drinksFrame.grid(row=3, column=0, columnspan=3,
                         sticky="nsew", padx=20, pady=20)
        drinksFrame.grid_columnconfigure(0, weight=1)
        drinksFrame.grid_columnconfigure(1, weight=1)
        drinksFrame.grid_columnconfigure(2, weight=1)

        drinks = price_calculator.prices_data
        stock = stock_manager.stock_data

        drinksCountInRow = 3
        drinksRowsCount = ceil(len(drinks) / drinksCountInRow)

        # Create drink buttons
        for idx, (drink, price) in enumerate(drinks.items()):
            buttonRow = idx // drinksCountInRow
            buttonColumn = idx % drinksCountInRow
            quantity = stock.get(drink, 0)

            buttonText = f"{drink} - {price:.2f}€ (Quantity: {quantity})"

            if stock_manager.is_in_stock(drink, 1):
                button = Button(drinksFrame, text=buttonText, command=lambda drink=drink,
                                price=price: add_drink(drink, price, stock_manager, update_ui))
            else:
                button = Button(drinksFrame, text=f"{
                                drink} - SOLD OUT", state=DISABLED)

            button.grid(column=buttonColumn,
                        row=buttonRow, sticky="ew", padx=2)

        # Create restock button at the bottom of the window, spanning all columns
        Button(root, text="Restock", command=open_admin_panel, font=("Arial", 16), width=20).grid(
            row=drinksRowsCount + 4, column=0, columnspan=3, pady=20, sticky="ew")

    def open_admin_panel():
        # Open admin panel with password protection
        password = simpledialog.askstring(
            "Enter Password", "Please enter the admin password:", show='*')
        if password == "123":
            admin_root = tk.Toplevel()
            admin_root.title("Admin Panel")
            admin_root.protocol("WM_DELETE_WINDOW", update_ui)
            AdminPanel(admin_root, stock_manager, price_calculator, update_ui)
            admin_root.mainloop()
        else:
            messagebox.showerror("Error", "Incorrect password!")

    build_ui()


def add_drink(drink, price, stock_manager, update_ui_callback):
    # Add drink to order and update stock
    global sumToEnter, guthaben
    if guthaben >= price:
        sumToEnter += price
        guthaben -= price  # Reduce the balance by the drink's price
        stock_manager.update_stock(drink, 1)
        update_labels()
        log_transaction(drink, 1, price, price)
        update_ui_callback()
    else:
        messagebox.showerror("Fehler", f"Nicht genug Guthaben. Preis: {
                             price:.2f}€, Guthaben: {guthaben:.2f}€")


def update_labels():
    # Update labels for entered sum, sum to enter, and change
    global guthabenLabel
    # Update balance label
    guthabenLabel.config(text=f"Guthaben: {guthaben:.2f}€")


def reset():
    # Reset all values and update labels
    global sumToEnter, enteredSum, change, guthaben
    sumToEnter = 0
    enteredSum = 0
    change = 0
    guthaben = 0
    update_labels()


def log_transaction(item, quantity, price, total):
    # Log transaction to CSV file
    global transaction_id
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transaction_data = [transaction_id, item,
                        quantity, price, total, timestamp]

    with open(os.path.join(os.path.dirname(__file__), '..', 'Backend', 'CSV', 'transactions.csv'), mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(transaction_data)

    transaction_id += 1


def enter_money(value):
    # Enter money and update balance label
    global guthabenLabel, guthaben
    guthaben += value
    guthabenLabel.config(text=f"Guthaben: {guthaben:.2f}€")


def reset_money():
    # Reset balance to zero and update balance label
    global guthabenLabel, guthaben
    guthaben = 0
    guthabenLabel.config(text="Guthaben: 0")
