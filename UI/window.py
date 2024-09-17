import tkinter as tk
from tkinter import Button, Label, DISABLED, simpledialog, messagebox
from math import ceil
import os
import csv
from datetime import datetime
from Backend.DataAccessors.Stock import Stock  # Korrekt importieren
from Backend.CSVHandler import CSVHandler
from Backend.Tools.PriceCalculator import PriceCalculator  # Importiere PriceCalculator
from UI.admin_panel import AdminPanel  # Importiere AdminPanel

# Globale Variablen initialisieren
global enteredSum, sumToEnter, change, transaction_id
global labelEnteredSum, labelSumToEnter, labelChange
enteredSum = 0
sumToEnter = 0
change = 0
transaction_id = 1

# Globale Variablen für Labels
labelEnteredSum = None
labelSumToEnter = None
labelChange = None

def create_window(root, price_calculator):
    global enteredSum, sumToEnter, change, transaction_id
    global labelEnteredSum, labelSumToEnter, labelChange

    csv_handler = CSVHandler()  # CSVHandler erstellen
    stock_file_path = os.path.join(os.path.dirname(__file__), '..', 'Backend', 'CSV', 'stock.csv')
    stock_manager = Stock(csv_handler, stock_file_path)  # Verwende die 'Stock'-Klasse

    # Methode zum Aktualisieren der UI
    def update_ui():
        # Entferne alle vorhandenen Widgets
        for widget in root.winfo_children():
            widget.destroy()
        # Erstelle die UI neu
        build_ui()

    # Funktion zum Erstellen der UI
    def build_ui():
        drinks = price_calculator.prices_data  # Preise aus prices.csv
        stock = stock_manager.stock_data  # Lagerbestand aus Stock.csv

        drinksCountInRow = 3
        drinksRowsCount = ceil(len(drinks) / drinksCountInRow)

        # Dynamische Generierung der Buttons basierend auf Produkte und Lagerbestand
        for idx, (drink, price) in enumerate(drinks.items()):
            buttonRow = idx // drinksCountInRow
            buttonColumn = idx % drinksCountInRow
            quantity = stock.get(drink, 0)  # Hole die Menge aus stock.csv

            # Button-Text, der Produktname, Preis und Menge anzeigt
            buttonText = f"{drink} - {price:.2f}€ (Menge: {quantity})"

            # Button aktivieren, wenn das Produkt auf Lager ist, sonst deaktiviert
            if stock_manager.is_in_stock(drink, 1):
                button = Button(root, text=buttonText, command=lambda drink=drink, price=price: add_drink(drink, price, stock_manager))
            else:
                button = Button(root, text=f"{drink} - AUSVERKAUFT", state=DISABLED)

            button.grid(row=buttonRow, column=buttonColumn)

        # Labels für den eingegebenen Betrag, den noch zu zahlenden Betrag und das Wechselgeld
        global labelEnteredSum, labelSumToEnter, labelChange
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

    # Admin-Panel öffnen und die UI aktualisieren, wenn ein neues Produkt hinzugefügt wird
    def open_admin_panel():
        password = simpledialog.askstring("Passwort eingeben", "Bitte das Admin-Passwort eingeben:", show='*')
        if password == "123": 
            # Admin-Panel öffnen
            admin_root = tk.Toplevel()
            admin_root.title("Admin Panel")
            csv_handler = CSVHandler()  # CSVHandler erstellen
            
            # Absoluter Pfad zur stock.csv
            stock_file_path = os.path.join(os.path.dirname(__file__), '..', 'Backend', 'CSV', 'stock.csv')
            stock_manager = Stock(csv_handler, stock_file_path)
            
            # Absoluter Pfad zur prices.csv
            prices_file_path = os.path.join(os.path.dirname(__file__), '..', 'Backend', 'CSV', 'prices.csv')
            price_calculator = PriceCalculator(csv_handler, prices_file_path)
            
            # AdminPanel mit price_calculator und stock_manager erstellen
            AdminPanel(admin_root, stock_manager, price_calculator, update_ui)  # Übergib die Callback-Methode
            admin_root.mainloop()
        else:
            messagebox.showerror("Fehler", "Falsches Passwort!")

    # Erstelle die UI beim Start
    build_ui()

def add_drink(drink, price, stock_manager):
    global sumToEnter
    sumToEnter += price

    # Verringere den Lagerbestand um 1
    stock_manager.update_stock(drink, 1)  # Verwende die 'update_stock'-Methode der 'Stock'-Klasse

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