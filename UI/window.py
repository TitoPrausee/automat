# UI/window.py

import tkinter as tk
from tkinter import Button, Entry, Label, DISABLED
from math import ceil

def create_window(root, price_calculator, stock_manager):
    enteredSum = 0
    sumToEnter = 0
    change = 0

    drinks = price_calculator.prices_data

    drinksCountInRow = 3
    drinksRowsCount = ceil(len(drinks) / drinksCountInRow)

    for idx, (drink, price) in enumerate(drinks.items()):
        buttonRow = idx // drinksCountInRow
        buttonColumn = idx % drinksCountInRow
        buttonText = f"{drink} - {price}€"

        if stock_manager.is_in_stock(drink, 1):
            button = Button(root, text=buttonText, command=lambda drink=drink, price=price: add_drink(drink, price, stock_manager, sumToEnter))
        else:
            button = Button(root, text=f"{drink} - AUSVERKAUFT", state=DISABLED)

        button.grid(row=buttonRow, column=buttonColumn)

    entry = Entry(root)
    entry.grid(row=drinksRowsCount + 0, column=1)
    Button(root, text="Eingeben", command=lambda: enter_sum(entry, sumToEnter)).grid(row=drinksRowsCount + 0, column=2)

    labelEnteredSum = Label(root, text="Eingegeben: 0")
    labelEnteredSum.grid(row=drinksRowsCount + 1, column=0)
    labelSumToEnter = Label(root, text="Noch einzugeben: 0")
    labelSumToEnter.grid(row=drinksRowsCount + 2, column=0)
    labelChange = Label(root, text="Ausgabe: 0")
    labelChange.grid(row=drinksRowsCount + 3, column=0)

    Button(root, text="Finish", command=reset).grid(row=drinksRowsCount + 4, column=0)

def add_drink(drink, price, stock_manager, sumToEnter):
    sumToEnter += price
    stock_manager.update_stock(drink, 1)
    update_labels()

def update_labels():
    global enteredSum, sumToEnter, change
    global labelEnteredSum, labelSumToEnter, labelChange
    
    change = enteredSum - sumToEnter if enteredSum >= sumToEnter else 0
    labelEnteredSum.config(text=f"Eingegeben: {enteredSum}")
    labelSumToEnter.config(text=f"Noch einzugeben: {max(sumToEnter - enteredSum, 0)}")
    labelChange.config(text=f"Ausgabe: {change}")



def enter_sum(entry, sumToEnter):
    value = int(entry.get())
    enteredSum += value
    update_labels()

def reset():
    sumToEnter = 0
    enteredSum = 0
    change = 0
    update_labels()
