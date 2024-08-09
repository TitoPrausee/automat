"""
Vending Machine GUI
====================
This script creates a simple GUI for a vending machine using Tkinter.
It allows the selection of drinks, entering of money, and displays the
change to be given.
"""

import sys
import os
from tkinter import *
from math import ceil, floor

# Füge den Python-Pfad hinzu, um das Backend-Modul zu finden
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importiere das Backend-Modul für Banknotenoperationen
from Backend.Tools.banknotes import supportedBanknotes, sumToBanknotes, formatBanknotes

# Global variables for managing the vending machine state
drinks = {
    "Cola": 2,
    "Water": 1,
    "Juice": 3,
    "Tea": 1.5,
    "Coffee": 2.5
}

maxCount = 1  # Maximum number of drinks that can be selected at once
count = 0  # Counter for selected drinks
sum = 0  # Total sum of selected drinks
enteredSum = 0  # Sum of money entered by the user
sumToEnter = 0  # Amount of money still needed to complete the transaction
change = 0  # Amount of change to be returned

# Create the main window
root = Tk()
root.title("Automat")  # Set window title
root.geometry('700x1000')  # Set window size (width x height)

# Layout configuration
drinksCountInRow = 3  # Number of drink buttons per row
drinksRowsCount = ceil(len(drinks) / drinksCountInRow)  # Number of rows needed for drink buttons

# Add drink selection buttons
for idx, (drink, price) in enumerate(drinks.items()):
    buttonText = f"{drink} - {price}€"
    buttonRow = floor(idx / drinksCountInRow)
    buttonColumn = idx % drinksCountInRow
    Button(root, text=buttonText, command=lambda price=price: addDrink(price)).grid(row=buttonRow, column=buttonColumn)

# List of supported banknotes
listOfPossibleBanknotes = ', '.join(str(x) for x in supportedBanknotes)

# Input field for entering money
Label(root, text=f"Geben Sie das Geld ein. Mögliche Scheine: {listOfPossibleBanknotes}").grid(row=drinksRowsCount + 0, column=0)
entry = Entry(root)
entry.grid(row=drinksRowsCount + 0, column=1)
Button(root, text="Eingeben", command=lambda: enterSum(int(entry.get()))).grid(row=drinksRowsCount + 0, column=2)

# Labels to display current state
labelEnteredSum = Label(root, text="Eingegeben: {}".format(enteredSum))
labelEnteredSum.grid(row=drinksRowsCount + 1, column=0)
labelSumToEnter = Label(root, text="Noch einzugeben: {}".format(sumToEnter))
labelSumToEnter.grid(row=drinksRowsCount + 2, column=0)
labelChange = Label(root, text=f"Ausgabe: {formatBanknotes(sumToBanknotes(change))}")
labelChange.grid(row=drinksRowsCount + 3, column=0)

# Finish button to reset the machine
Button(root, text="Finish", command=lambda: reset()).grid(row=drinksRowsCount + 4, column=0)


def addDrink(price):
    """
    Add a drink's price to the total if the maximum count is not reached.

    :param price: The price of the selected drink.
    """
    global sum, maxCount, count
    if count < maxCount:
        sum += price  # Add the drink price to the total sum
        count += 1  # Increase the count of selected drinks
        updateLabels()  # Update the labels to reflect the new state


def updateLabels():
    """
    Update the GUI labels to reflect the current transaction state.
    """
    global sum, enteredSum, sumToEnter, change
    sumToEnter = max(sum - enteredSum, 0)  # Calculate the remaining amount to enter
    change = max(enteredSum - sum, 0)  # Calculate the change to be returned

    labelEnteredSum.config(text=f"Eingegeben: {enteredSum}")
    labelSumToEnter.config(text=f"Noch einzugeben: {sumToEnter}")
    labelChange.config(text=f"Ausgabe: {formatBanknotes(sumToBanknotes(change))}")


def enterSum(value):
    """
    Handle money entry, updating the total entered sum.

    :param value: The monetary value entered by the user.
    """
    if value in supportedBanknotes:
        global enteredSum
        enteredSum += value  # Add the entered value to the total entered sum
        updateLabels()  # Update the labels to reflect the new state


def reset():
    """
    Reset the vending machine to its initial state.
    """
    global sum, enteredSum, count, maxCount, change
    sum = 0
    enteredSum = 0
    count = 0
    maxCount = 1
    change = 0
    updateLabels()  # Update the labels to reflect the reset state


# Start the Tkinter main loop
root.mainloop()
