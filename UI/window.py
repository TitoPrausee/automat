import tkinter as tk
from tkinter import Button, Label, DISABLED, simpledialog, messagebox
from math import ceil
import os
import csv
from datetime import datetime
from Backend.DataAccessors.Stock import Stock
from Backend.CSVHandler import CSVHandler
from UI.admin_panel import AdminPanel

# Globale Variableninitialisierung
global enteredSum, sumToEnter, change, transaction_id, guthaben, totalEntered, ordered_drinks
# Initialisierung der globalen Variablen
guthaben = 0
enteredSum = 0
sumToEnter = 0
change = 0
transaction_id = 1
totalEntered = 0
ordered_drinks = {}

# Globale Variablen für Labels
guthabenLabel = None
changeLabel = None

def create_window(root, price_calculator):
    """
    Erstellt das Hauptfenster der Anwendung, in dem die Getränke angezeigt werden.

    :param root: Das Tkinter-Hauptfenster.
    :param price_calculator: Instanz der PriceCalculator-Klasse zur Verwaltung der Produktpreise.
    """
    global enteredSum, sumToEnter, change, transaction_id, guthaben, totalEntered, ordered_drinks
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
        # Konfiguriert die Grid-Spalten
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Setzt die automatische Größenanpassung zurück
        root.grid_propagate(True)

        # Erstellt Titel-Label
        Label(root, text="Getränkeautomat", font=("Arial", 22)).grid(
            row=0, column=1, padx=10)

        # Erstellt Guthaben-Label
        guthabenLabel = Label(root, text=f"Guthaben: {guthaben:.2f}€", font=("Arial", 20))
        guthabenLabel.grid(row=1, column=1, pady=10)

        # Erstellt Rahmen für Geldknöpfe
        moneyFrame = tk.Frame(root, bg="white", borderwidth=2, relief="sunken")
        moneyFrame.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        moneyFrame.grid_columnconfigure(0, weight=1)
        moneyFrame.grid_columnconfigure(1, weight=1)
        moneyFrame.grid_columnconfigure(2, weight=1)

        # Münzknöpfe
        coin_values = [0.5, 1, 2]
        for i, coin in enumerate(coin_values):
            Button(moneyFrame, highlightbackground="white", width=8, text=f"{coin}€",
                   command=lambda value=coin: enter_money(value), cursor="hand2").grid(row=0, column=i, sticky="ew")

        # Schein-Knöpfe
        bill_values = [10, 5, 20]
        for i, bill in enumerate(bill_values):
            Button(moneyFrame, highlightbackground="white", width=8, text=f"{bill}€",
                   command=lambda value=bill: enter_money(value), cursor="hand2").grid(row=1, column=i, sticky="ew")

        # Rahmen für Getränkeknöpfe
        drinksFrame = tk.Frame(root, bg="white", borderwidth=2, relief="sunken")
        drinksFrame.grid(row=3, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        drinksFrame.grid_columnconfigure(0, weight=1)
        drinksFrame.grid_columnconfigure(1, weight=1)
        drinksFrame.grid_columnconfigure(2, weight=1)

        drinks = price_calculator.prices_data
        stock = stock_manager.stock_data

        drinksCountInRow = 3
        drinksRowsCount = ceil(len(drinks) / drinksCountInRow)

        # Getränkeknöpfe
        for idx, (drink, price) in enumerate(drinks.items()):
            buttonRow = idx // drinksCountInRow
            buttonColumn = idx % drinksCountInRow
            quantity = stock.get(drink, 0)

            buttonText = f"{drink} - {price:.2f}€ (Quantity: {quantity})"

            if stock_manager.is_in_stock(drink, 1):
                button = Button(drinksFrame, text=buttonText, command=lambda drink=drink,
                                price=price: add_drink(drink, price, stock_manager, update_ui), cursor="hand2")
            else:
                button = Button(drinksFrame, text=f"{drink} - SOLD OUT", state=DISABLED)

            button.grid(column=buttonColumn, row=buttonRow, sticky="ew")

        # Create bottom action buttons
        Button(root, text="Wartung", command=open_admin_panel, font=("Arial", 16), width=20).grid(
            row=drinksRowsCount + 4, column=0, pady=20, sticky="ew")
        Button(root, text="Ausgabe", command=complete_transaction, font=("Arial", 16), width=20).grid(
            row=drinksRowsCount + 4, column=1, pady=20, sticky="ew")
        Button(root, text="Abbrechen", command=lambda: cancel_transaction(update_ui), font=("Arial", 16), width=20).grid(
            row=drinksRowsCount + 4, column=2, pady=20, sticky="ew")

        # Rückgeld-Label
        changeLabel = Label(root, text=f"Rückgeld: {change:.2f}€", font=("Arial", 16))
        changeLabel.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

        # Minimale Fenstergröße
        root.update_idletasks()
        min_width = root.winfo_reqwidth()
        min_height = root.winfo_reqheight()
        root.minsize(min_width, min_height)
        root.maxsize(height=60)  # adjust the height value to your liking

    def open_admin_panel():
        """
        Öffnet das Admin-Panel, nachdem das korrekte Passwort eingegeben wurde.
        """
        password = simpledialog.askstring("Enter Password", "Please enter the admin password:", show='*')
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
    global sumToEnter, guthaben, ordered_drinks
    if guthaben >= price:
        sumToEnter += price
        guthaben -= price
        stock_manager.update_stock(drink, 1)

        # Track the ordered drink in the dictionary
        if drink in ordered_drinks:
            ordered_drinks[drink] += 1
        else:
            ordered_drinks[drink] = 1

        update_labels()
        log_transaction(drink, 1, price, price)
        update_ui_callback()
    else:
        messagebox.showerror("Fehler", f"Nicht genug Guthaben. Preis: {price:.2f}€, Guthaben: {guthaben:.2f}€")

def complete_transaction():
    """
    Schließt die aktuelle Transaktion ab, gibt Wechselgeld zurück und zeigt eine Bestätigungsnachricht an.
    """
    global guthaben, change, ordered_drinks, totalEntered
    change = guthaben
    guthaben = 0
    totalEntered = 0
    ordered_drinks = {}
    update_labels()
    messagebox.showinfo("Transaktion abgeschlossen", f"Rückgeld: {change:.2f}€")
    change = 0  # Setzt das Wechselgeld nach der Anzeige der Nachricht zurück

def cancel_transaction(update_ui):
    # Cancel the transaction, return all money, and restore stock
    global guthaben, change, ordered_drinks, totalEntered

    csv_handler = CSVHandler()
    stock_file_path = os.path.join(os.path.dirname(__file__), '..', 'Backend', 'CSV', 'stock.csv')
    stock_manager = Stock(csv_handler, stock_file_path)

    # Return the stock of the ordered drinks
    for drink, quantity in ordered_drinks.items():
        stock_manager.update_stock(drink, -quantity)  # Restock the ordered items

    # Reset the ordered drinks dictionary
    ordered_drinks = {}

    # Handle the refund and UI updates
    change = totalEntered
    guthaben = 0
    update_labels()
    messagebox.showinfo("Transaktion abgebrochen", f"Rückgeld: {totalEntered:.2f}€")
    update_ui()
    change = 0
    totalEntered = 0  # Reset after showing message

def update_labels():
    """
    Aktualisiert die Labels für das aktuelle Guthaben und das Rückgeld.
    """
    global guthabenLabel, changeLabel
    guthabenLabel.config(text=f"Guthaben: {guthaben:.2f}€")
    changeLabel.config(text=f"Rückgeld: {change:.2f}€")

def log_transaction(item, quantity, price, total):
    """
    Protokolliert eine abgeschlossene Transaktion mit Zeitstempel in einer CSV-Datei.

    :param item: Der Name des gekauften Artikels.
    :param quantity: Die gekaufte Menge des Artikels.
    :param price: Der Preis pro Einheit des Artikels.
    :param total: Der Gesamtpreis der Transaktion.
    """
    global transaction_id
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transaction_data = [transaction_id, item, quantity, price, total, timestamp]

    with open(os.path.join(os.path.dirname(__file__), '..', 'Backend', 'CSV', 'transactions.csv'), mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(transaction_data)

    transaction_id += 1

def enter_money(value):
    # Enter money and update balance label
    global guthabenLabel, guthaben, totalEntered
    totalEntered+= value
    guthaben += value
    guthabenLabel.config(text=f"Guthaben: {guthaben:.2f}€")

def reset_money():
    """
    Setzt das aktuelle Guthaben auf null zurück und aktualisiert das Guthaben-Label entsprechend.
    """
    global guthabenLabel, guthaben
    guthaben = 0
    guthabenLabel.config(text="Guthaben: 0")