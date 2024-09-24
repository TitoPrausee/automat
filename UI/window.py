import tkinter as tk
from tkinter import Button, Label, DISABLED, simpledialog, messagebox
from math import ceil
import os
import csv
from datetime import datetime
from Backend.DataAccessors.Stock import Stock
from Backend.CSVHandler import CSVHandler
from Backend.DataAccessors.Transaction import Transaction
from UI.admin_panel import AdminPanel

# Globale Variableninitialisierung
global enteredSum, sumToEnter, change, guthaben, ordered_drinks, totalEntered
global guthabenLabel, drinksFrame, changeLabel
guthaben = 0  # Aktuelles Guthaben des Nutzers
enteredSum = 0  # Gesamtsumme der eingegebenen Gelder
sumToEnter = 0  # Summe, die für die aktuelle Transaktion eingegeben wurde
change = 0  # Rückgeld
totalEntered = 0  # Gesamtbetrag, der eingegeben wurde
ordered_drinks = {}  # Bestellte Getränke und deren Mengen

# Globale Variablen für Labels
guthabenLabel = None
changeLabel = None

def create_window(root, price_calculator):
    """
    Erstellt das Hauptfenster der Anwendung, in dem die Getränke angezeigt werden.

    :param root: Das Tkinter-Hauptfenster.
    :param price_calculator: Instanz der PriceCalculator-Klasse zur Verwaltung der Produktpreise.
    """
    global enteredSum, sumToEnter, change, guthaben
    global guthabenLabel, changeLabel

    csv_handler = CSVHandler()
    stock_file_path = os.path.join(os.path.dirname(__file__), '..', 'Backend', 'CSV', 'stock.csv')
    stock_manager = Stock(csv_handler, stock_file_path)

    def update_ui():
        """
        Aktualisiert die Benutzeroberfläche, indem alle Widgets gelöscht und die UI neu aufgebaut wird.
        """
        for widget in root.winfo_children():
            widget.destroy()
        build_ui()

    def build_ui():
        """
        Baut die Benutzeroberfläche des Hauptfensters auf, einschließlich der Anzeige von Getränken,
        des Guthabens, der Eingabemöglichkeiten für Geld und der Aktionsschaltflächen.
        """
        global guthabenLabel, changeLabel
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_propagate(True)

        Label(root, text="Getränkeautomat", font=("Arial", 22)).grid(row=0, column=1, padx=10)
        guthabenLabel = Label(root, text=f"Guthaben: {guthaben:.2f}€", font=("Arial", 20))
        guthabenLabel.grid(row=1, column=1, pady=10)

        moneyFrame = tk.Frame(root, bg="white", borderwidth=2, relief="sunken")
        moneyFrame.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        moneyFrame.grid_columnconfigure(0, weight=1)
        moneyFrame.grid_columnconfigure(1, weight=1)
        moneyFrame.grid_columnconfigure(2, weight=1)

        coin_values = [0.5, 1, 2]
        for i, coin in enumerate(coin_values):
            Button(moneyFrame, highlightbackground="white", width=8, text=f"{coin}€",
                   command=lambda value=coin: enter_money(value), cursor="hand2").grid(row=0, column=i, sticky="ew")

        bill_values = [10, 5, 20]
        for i, bill in enumerate(bill_values):
            Button(moneyFrame, highlightbackground="white", width=8, text=f"{bill}€",
                   command=lambda value=bill: enter_money(value), cursor="hand2").grid(row=1, column=i, sticky="ew")

        drinksFrame = tk.Frame(root, bg="white", borderwidth=2, relief="sunken")
        drinksFrame.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        drinksFrame.grid_columnconfigure(0, weight=1)
        drinksFrame.grid_columnconfigure(1, weight=1)
        drinksFrame.grid_columnconfigure(2, weight=1)

        drinks = price_calculator.prices_data
        stock = stock_manager.stock_data

        drinksCountInRow = 3
        drinksRowsCount = ceil(len(drinks) / drinksCountInRow)

        for idx, (drink, price) in enumerate(drinks.items()):
            buttonRow = idx // drinksCountInRow
            buttonColumn = idx % drinksCountInRow
            quantity = stock.get(drink, 0)

            buttonText = f"{drink} - {price:.2f}€ (Quantity: {quantity})"

            if stock_manager.is_in_stock(drink, 1):
                button = Button(drinksFrame, text=buttonText, command=lambda drink=drink,
                                price=price: add_drink(drink, price, stock_manager, update_ui), cursor="hand2")
            else:
                button = Button(drinksFrame, text=f"{drink} - Ausverkauft", state=DISABLED)

            button.grid(column=buttonColumn, row=buttonRow, sticky="ew")

        Button(root, text="Wartung", command=open_admin_panel, font=("Arial", 16), width=10, cursor="hand2").grid(
            row=4, column=0, pady=10, padx=10, sticky="ew")
        Button(root, text="Ausgabe", command=complete_transaction, font=("Arial", 16), width=10, cursor="hand2").grid(
            row=4, column=1, pady=10, padx=10, sticky="ew")
        Button(root, text="Abbrechen", command=lambda: cancel_transaction(update_ui), font=("Arial", 16), width=10, cursor="hand2").grid(
            row=4, column=2, pady=10, padx=10, sticky="ew")

        changeLabel = Label(root, text=f"Rückgeld: {change:.2f}€", font=("Arial", 16))
        changeLabel.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

        root.update_idletasks()
        min_width = root.winfo_reqwidth()
        min_height = root.winfo_reqheight()
        root.minsize(min_width, min_height)
        root.maxsize(height=600)

    def open_admin_panel():
        dirname = os.path.dirname(os.path.dirname(__file__))
     
        pp = os.path.join(dirname, 'password.txt')
        f = open(pp, "r")

        password = simpledialog.askstring("Enter Password", "Please enter the admin password:", show='*')
        if password == f.read():
            admin_root = tk.Toplevel()
            admin_root.title("Admin Panel")
            admin_root.protocol("WM_DELETE_WINDOW", update_ui)
            AdminPanel(admin_root, stock_manager, price_calculator, update_ui)
            admin_root.mainloop()
        else:
            messagebox.showerror("Fehler", "Falsches Passwort!")

    build_ui()

def add_drink(drink, price, stock_manager, update_ui_callback):
    global sumToEnter, guthaben, ordered_drinks
    if guthaben >= price:
        sumToEnter += price
        guthaben -= price
        stock_manager.update_stock(drink, 1)

        # Bestellte Getränke verfolgen
        ordered_drinks[drink] = ordered_drinks.get(drink, 0) + 1

        update_labels()
        log_transaction(drink, 1, price, price)
        update_ui_callback()
    else:
        messagebox.showerror("Fehler", f"Nicht genug Guthaben. Preis: {price:.2f}€, Guthaben: {guthaben:.2f}€")

def complete_transaction():
    global guthaben, change, ordered_drinks, totalEntered
    change = guthaben
    guthaben = 0
    totalEntered = 0
    ordered_drinks = {}
    update_labels()
    messagebox.showinfo("Transaktion abgeschlossen", f"Rückgeld: {change:.2f}€")
    change = 0

def cancel_transaction(update_ui):
    global guthaben, change, ordered_drinks, totalEntered

    csv_handler = CSVHandler()
    stock_file_path = os.path.join(os.path.dirname(__file__), '..', 'Backend', 'CSV', 'stock.csv')
    stock_manager = Stock(csv_handler, stock_file_path)

    # Rückstocken der bestellten Getränke
    for drink, quantity in ordered_drinks.items():
        stock_manager.update_stock(drink, -quantity)

    # Zurücksetzen der bestellten Getränke
    ordered_drinks = {}

    change = totalEntered
    guthaben = 0
    update_labels()
    messagebox.showinfo("Transaktion abgebrochen", f"Rückgeld: {totalEntered:.2f}€")

    # UI aktualisieren, um die Bestandsänderungen anzuzeigen
    update_ui()

    change = 0
    totalEntered = 0

def update_labels():
    global guthabenLabel, changeLabel
    guthabenLabel.config(text=f"Guthaben: {guthaben:.2f}€")
    changeLabel.config(text=f"Rückgeld: {change:.2f}€")

def log_transaction(item, quantity, price, total):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transaction_data = {'item': item, 'quantity': quantity, 'price': price, 'total': total, 'timestamp': timestamp}

    Transaction.Save(transaction_data)
   
    

def enter_money(value):
    global guthabenLabel, guthaben, totalEntered
    guthaben += value
    totalEntered += value
    guthabenLabel.config(text=f"Guthaben: {guthaben:.2f}€")

def reset_money():
    global guthabenLabel, guthaben
    guthaben = 0
    guthabenLabel.config(text="Guthaben: 0€")