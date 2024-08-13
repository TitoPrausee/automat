import sys
import os
import tkinter as tk
from tkinter import Tk, Button, Entry, Label, DISABLED
from math import ceil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'Backend')))

from Backend.Tools.PriceCalculator import PriceCalculator
from Backend.DataAccessors.Stock import Stock
from Backend.Tools.CSVHandler import CSVHandler

def main():
    csv_handler = CSVHandler()
    price_calculator = PriceCalculator(csv_handler, 'CSV/prices.csv')
    stock_manager = Stock(csv_handler, 'CSV/stock.csv')

    drinks = price_calculator.prices_data

    root = Tk()

    root.title("Automat")
    root.geometry('700x1000')

    global enteredSum, sumToEnter, change, labelEnteredSum, labelSumToEnter, labelChange
    enteredSum = 0
    sumToEnter = 0
    change = 0

    drinksCountInRow = 3
    drinksRowsCount = ceil(len(drinks) / drinksCountInRow)

    for idx, (drink, price) in enumerate(drinks.items()):
        buttonRow = idx // drinksCountInRow
        buttonColumn = idx % drinksCountInRow
        buttonText = f"{drink} - {price}€"

        if stock_manager.is_in_stock(drink, 1):
            button = Button(root, text=buttonText, command=lambda drink=drink, price=price: addDrink(drink, price, stock_manager))
        else:
            button = Button(root, text=f"{drink} - AUSVERKAUFT", state=DISABLED)

        button.grid(row=buttonRow, column=buttonColumn)

    entry = Entry(root)
    entry.grid(row=drinksRowsCount + 0, column=1)
    Button(root, text="Eingeben", command=lambda: enterSum(int(entry.get()))).grid(row=drinksRowsCount + 0, column=2)

    labelEnteredSum = Label(root, text="Eingegeben: 0")
    labelEnteredSum.grid(row=drinksRowsCount + 1, column=0)
    labelSumToEnter = Label(root, text="Noch einzugeben: 0")
    labelSumToEnter.grid(row=drinksRowsCount + 2, column=0)
    labelChange = Label(root, text="Ausgabe: 0")
    labelChange.grid(row=drinksRowsCount + 3, column=0)

    Button(root, text="Finish", command=reset).grid(row=drinksRowsCount + 4, column=0)

    root.mainloop()

def addDrink(drink, price, stock_manager):
    global sumToEnter
    sumToEnter += price
    stock_manager.update_stock(drink, 1)
    updateLabels()

def updateLabels():
    global sumToEnter, enteredSum, change
    change = enteredSum - sumToEnter if enteredSum >= sumToEnter else 0
    labelEnteredSum.config(text=f"Eingegeben: {enteredSum}")
    labelSumToEnter.config(text=f"Noch einzugeben: {max(sumToEnter - enteredSum, 0)}")
    labelChange.config(text=f"Ausgabe: {change}")

def enterSum(value: int):
    global enteredSum
    enteredSum += value
    updateLabels()

def reset():
    global sumToEnter, enteredSum, change
    sumToEnter = 0
    enteredSum = 0
    change = 0
    updateLabels()

if __name__ == "__main__":
    main()
