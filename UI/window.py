# UI/window.py

import tkinter as tk
from tkinter import Button, Entry, Label, DISABLED
from math import ceil
import csv
from datetime import datetime

# 1. Globale Variablen initialisieren
global enteredSum, sumToEnter, change, transaction_id
global labelEnteredSum, labelSumToEnter, labelChange

enteredSum = 0
sumToEnter = 0
change = 0
transaction_id = 1  # Starten bei 1 für die erste Transaktion

# 2. Hauptfunktion zur Erstellung des Fensters
def create_window(root, price_calculator, stock_manager):
    global labelEnteredSum, labelSumToEnter, labelChange
    
    # Getränke-Daten abrufen
    drinks = price_calculator.prices_data

    # Berechnung der Anordnung der Getränke-Buttons
    drinksCountInRow = 3
    drinksRowsCount = ceil(len(drinks) / drinksCountInRow)

    # Getränke-Buttons erstellen
    for idx, (drink, price) in enumerate(drinks.items()):
        buttonRow = idx // drinksCountInRow
        buttonColumn = idx % drinksCountInRow
        buttonText = f"{drink} - {price}€"

        # Button je nach Verfügbarkeit erstellen
        if stock_manager.is_in_stock(drink, 1):
            button = Button(
                root, 
                text=buttonText, 
                command=lambda drink=drink, price=price: add_drink(drink, price, stock_manager)
            )
        else:
            button = Button(root, text=f"{drink} - AUSVERKAUFT", state=DISABLED)

        button.grid(row=buttonRow, column=buttonColumn)

    # Eingabefeld und Buttons für die Benutzerinteraktion
    entry = Entry(root)
    entry.grid(row=drinksRowsCount, column=1)
    Button(root, text="Eingeben", command=lambda: enter_sum(entry)).grid(row=drinksRowsCount, column=2)

    # Labels für den aktuellen Status
    labelEnteredSum = Label(root, text="Eingegeben: 0")
    labelEnteredSum.grid(row=drinksRowsCount + 1, column=0)
    labelSumToEnter = Label(root, text="Noch einzugeben: 0")
    labelSumToEnter.grid(row=drinksRowsCount + 2, column=0)
    labelChange = Label(root, text="Ausgabe: 0")
    labelChange.grid(row=drinksRowsCount + 3, column=0)

    # Button zum Abschluss der Transaktion
    Button(root, text="Finish", command=reset).grid(row=drinksRowsCount + 4, column=0)

# 3. Funktionen für die Verarbeitung der Eingaben und Updates
def add_drink(drink, price, stock_manager):
    global sumToEnter
    
    # Preis zur zu zahlenden Summe hinzufügen
    sumToEnter += price
    stock_manager.update_stock(drink, 1)
    update_labels()
    
    # Transaktion loggen
    log_transaction(drink, 1, price, price)

def update_labels():
    global enteredSum, sumToEnter, change
    
    # Berechnung des Rückgeldes
    change = enteredSum - sumToEnter if enteredSum >= sumToEnter else 0
    
    # Labels aktualisieren
    labelEnteredSum.config(text=f"Eingegeben: {enteredSum}")
    labelSumToEnter.config(text=f"Noch einzugeben: {max(sumToEnter - enteredSum, 0)}")
    labelChange.config(text=f"Ausgabe: {change}")

def enter_sum(entry):
    global enteredSum
    try:
        # Benutzereingabe in eine Zahl umwandeln
        value = float(entry.get())
        enteredSum += value
        update_labels()
    except ValueError:
        print("Ungültige Eingabe. Bitte eine Zahl eingeben.")

def reset():
    global sumToEnter, enteredSum, change
    
    # Zurücksetzen aller relevanten Variablen
    sumToEnter = 0
    enteredSum = 0
    change = 0
    update_labels()

# 4. Funktion zum Loggen der Transaktionen
def log_transaction(item, quantity, price, total):
    global transaction_id
    
    # Zeitstempel der Transaktion erstellen
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transaction_data = [transaction_id, item, quantity, price, total, timestamp]
    
    # Transaktionsdaten in die CSV-Datei schreiben
    with open('Backend/CSV/transactions.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(transaction_data)

    # Transaktions-ID erhöhen
    transaction_id += 1
