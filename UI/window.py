# UI/window.py

import tkinter as tk
from tkinter import Button, Label, DISABLED, simpledialog, messagebox, Frame
from math import ceil
import csv
import os
from UI.admin_panel import AdminPanel
from datetime import datetime
from Backend.DataAccessors.Stock import Stock
from Backend.CSVHandler import CSVHandler

# Globale Variablen initialisieren
global enteredSum, sumToEnter, change, transaction_id, guthaben
global labelEnteredSum, labelSumToEnter, labelChange
guthaben = 0
enteredSum = 0
sumToEnter = 0
change = 0
transaction_id = 1  

def create_UI(root, price_calculator, stock_manager):
    
    root.grid_columnconfigure(0, weight=1)  # Column 0
    root.grid_columnconfigure(1, weight=1)  # Column 1 (centered labels will be here)
    root.grid_columnconfigure(2, weight=1)  # Column 2

    
    Label(root, text="Getränkeautomat", font=("Arial", 22)).grid(row=0, column=1, sticky="NSEW", padx=10)

    guthabenLabel = Label(
        root,
        text="Guthaben: " + guthaben.__str__(),
        font=("Arial", 20),
        ).grid(row=1, column=1, pady=30, sticky="NESW")

    moneyFrame = tk.Frame(root, bg="white", borderwidth=2, relief="sunken", height=250)
    moneyFrame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)
    moneyFrame.grid_columnconfigure(0, weight=1)
    moneyFrame.grid_columnconfigure(1, weight=1)
    moneyFrame.grid_columnconfigure(2, weight=1)

    drinksFrame = tk.Frame(root, bg="white", borderwidth=2, relief="sunken", height=250)
    drinksFrame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)
    drinksFrame.grid_columnconfigure(0, weight=1)
    drinksFrame.grid_columnconfigure(1, weight=1)
    drinksFrame.grid_columnconfigure(2, weight=1)

    Button(root, text="Ausgabe", state=DISABLED).grid(row=4, column=1, sticky="ns", pady=10)

    # assigning this button to col1 shifts the whole UI to the right for some reason
    Button(root, text="Wartung").grid(row=5, column=1, padx=20)

def create_window(root, price_calculator, stock_manager):
    global enteredSum, sumToEnter, change, transaction_id
    global labelEnteredSum, labelSumToEnter, labelChange

    drinks = price_calculator.prices_data

    drinksCountInRow = 3
    drinksRowsCount = ceil(len(drinks) / drinksCountInRow)

    for idx, (drink, price) in enumerate(drinks.items()):
        buttonRow = idx // drinksCountInRow
        buttonColumn = idx % drinksCountInRow
        buttonText = f"{drink} - {price}€"

        if stock_manager.is_in_stock(drink, 1):
            button = Button(root, text=buttonText, command=lambda drink=drink, price=price: add_drink(drink, price, stock_manager))
        else:
            button = Button(root, text=f"{drink} - AUSVERKAUFT", state=DISABLED)

        button.grid(row=buttonRow, column=buttonColumn)

    labelEnteredSum = Label(root, text="Eingegeben: 0")
    labelEnteredSum.grid(row=drinksRowsCount + 1, column=0)
    labelSumToEnter = Label(root, text="Noch einzugeben: 0")
    labelSumToEnter.grid(row=drinksRowsCount + 2, column=0)
    labelChange = Label(root, text="Ausgabe: 0")
    labelChange.grid(row=drinksRowsCount + 3, column=0)

    # Geld-Eingabe Buttons für Münzen
    coin_values = [0.5, 1, 2]
    for i, coin in enumerate(coin_values):
        Button(root, text=f"{coin}€", command=lambda value=coin: enter_sum(value)).grid(row=drinksRowsCount + 4, column=i)

    # Geld-Eingabe Buttons für Scheine
    bill_values = [10, 20]
    for i, bill in enumerate(bill_values):
        Button(root, text=f"{bill}€", command=lambda value=bill: enter_sum(value)).grid(row=drinksRowsCount + 5, column=i)

    Button(root, text="Finish", command=reset).grid(row=drinksRowsCount + 6, column=0)

    # Auffüllen-Button für Admin-Zugang
    Button(root, text="Auffüllen", command=open_admin_panel).grid(row=drinksRowsCount + 7, column=0)

def add_drink(drink, price, stock_manager):
    global sumToEnter
    sumToEnter += price
    stock_manager.update_stock(drink, 1)
    update_labels()
    log_transaction(drink, 1, price, price)  # Loggt die Transaktion, 1 Menge pro Klick

def update_labels():
    global enteredSum, sumToEnter, change
    global labelEnteredSum, labelSumToEnter, labelChange
    
    change = enteredSum - sumToEnter if enteredSum >= sumToEnter else 0
    labelEnteredSum.config(text=f"Eingegeben: {enteredSum}")
    labelSumToEnter.config(text=f"Noch einzugeben: {max(sumToEnter - enteredSum, 0)}")
    labelChange.config(text=f"Ausgabe: {change}")

def enter_sum(value):
    global enteredSum
    enteredSum += value
    update_labels()

def reset():
    global sumToEnter, enteredSum, change
    sumToEnter = 0
    enteredSum = 0
    change = 0
    update_labels()

def log_transaction(item, quantity, price, total):
    global transaction_id
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transaction_data = [transaction_id, item, quantity, price, total, timestamp]
    
    # Transaktionsdaten in die CSV-Datei schreiben
    with open(os.path.join(os.path.dirname(__file__), '..', 'Backend', 'CSV', 'transactions.csv'), mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(transaction_data)

    transaction_id += 1  

def open_admin_panel():
    # Passwortabfrage
    password = simpledialog.askstring("Passwort eingeben", "Bitte das Admin-Passwort eingeben:", show='*')
    if password == "123": 
        # Admin-Panel öffnen
        admin_root = tk.Toplevel()
        admin_root.title("Admin Panel")
        csv_handler = CSVHandler()  # CSVHandler erstellen
        
        # Absoluter Pfad zur stock.csv
        file_path = os.path.join(os.path.dirname(__file__), '..', 'Backend', 'CSV', 'stock.csv')
        
        stock_manager = Stock(csv_handler, file_path)
        AdminPanel(admin_root, stock_manager)
        admin_root.mainloop()
    else:
        messagebox.showerror("Fehler", "Falsches Passwort!")
