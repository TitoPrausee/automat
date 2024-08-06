# Import Module
from tkinter import *
from math import ceil, floor

from Tools.banknotes import supportedBanknotes, sumToBanknotes, formatBanknotes

drinks = {
    "Cola": 2,
    "Water": 1,
    "Juice": 3,
    "Tea": 1.5,
    "Coffee": 2.5
}

sum = 0
enteredSum = 0
sumToEnter = 0
change = 0

# create root window
root = Tk()

# root window title and dimension
root.title("Automat")
# Set geometry (widthxheight)
root.geometry('700x1000')


# Add drink buttons
drinksCountInRow = 3
drinksRowsCount = ceil(len(drinks) / drinksCountInRow)
for idx, (drink, price) in enumerate(drinks.items()):
    buttonText = f"{drink} - {price}€"
    buttonRow = floor(idx/drinksCountInRow)
    buttonColumn = ceil(idx % drinksCountInRow)
    Button(root, text=buttonText, command=lambda price=price: addDrink(
        price)).grid(row=buttonRow, column=buttonColumn)

listOfPossibleBanknotes = ', '.join(str(x) for x in supportedBanknotes)

# Input field
Label(root, text=f"Geben Sie die Banknote ein. Mögliche Banknoten: {listOfPossibleBanknotes}").grid(
    row=drinksRowsCount + 0, column=0)
entry = Entry(root)
entry.grid(row=drinksRowsCount + 0, column=1)
Button(root, text="Eingeben", command=lambda: enterSum(
    int(entry.get()))).grid(row=drinksRowsCount + 0, column=2)

# Info labels
labelEnteredSum = Label(root, text="Eingegeben: {}".format(enteredSum))
labelEnteredSum.grid(
    row=drinksRowsCount + 1, column=0)
labelSumToEnter = Label(root, text="Noch einzugeben: {}".format(
    sumToEnter))
labelSumToEnter.grid(row=drinksRowsCount + 2, column=0)
labelChange = Label(root, text=f"Ausgabe: {
                    formatBanknotes(sumToBanknotes(change))}")
labelChange.grid(
    row=drinksRowsCount + 3, column=0)

# Finish button
Button(root, text="Finish").grid(row=drinksRowsCount + 4, column=0)


def addDrink(price):
    global sum
    sum += price
    updateLabels()


def updateLabels():
    global sum, enteredSum, sumToEnter, change
    sumToEnter = sum - enteredSum if sum - enteredSum >= 0 else 0
    change = enteredSum - sum if enteredSum - sum >= 0 else 0

    labelEnteredSum.config(text=f"Eingegeben: {enteredSum}")
    labelSumToEnter.config(text=f"Noch einzugeben: {sumToEnter}")
    labelChange.config(
        text=f"Ausgabe: {formatBanknotes(sumToBanknotes(change))}")


def enterSum(value):
    if (int(value) in supportedBanknotes):
        global enteredSum
        enteredSum += value
        updateLabels()


# all widgets will be here
# Execute Tkinter
root.mainloop()
