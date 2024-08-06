# Import Module
from tkinter import *
from math import ceil, floor

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
    Button(root, text=f"{drink} - ${price}", command=lambda price=price: addDrink(
        price)).grid(row=floor(idx/drinksCountInRow), column=ceil(idx % drinksCountInRow))

Label(root, text="Eingabe").grid(row=drinksRowsCount + 0, column=0)
entry = Entry(root)
entry.grid(row=drinksRowsCount + 0, column=1)
Button(root, text="Eingeben", command=lambda: enterSum(
    int(entry.get()))).grid(row=drinksRowsCount + 0, column=2)

Label(root, text="Eingegeben: {}".format(enteredSum)).grid(
    row=drinksRowsCount + 1, column=0)
Label(root, text="Noch einzugeben: {}".format(
    sumToEnter)).grid(row=drinksRowsCount + 2, column=0)

Label(root, text="Ausgabe: {}".format(change)).grid(
    row=drinksRowsCount + 3, column=0)

Button(root, text="Finish").grid(row=drinksRowsCount + 4, column=0)


def addDrink(price):
    global sum
    sum += price
    updateLabels()


def updateLabels():
    global sum, enteredSum, sumToEnter, change
    sumToEnter = sum - enteredSum if sum - enteredSum >= 0 else 0
    change = enteredSum - sum if enteredSum - sum >= 0 else 0

    Label(root, text="Eingegeben: {}".format(
        enteredSum)).grid(row=drinksRowsCount + 1, column=0)
    Label(root, text="Noch einzugeben: {}".format(
        sumToEnter)).grid(row=drinksRowsCount + 2, column=0)
    Label(root, text="Ausgabe: {}".format(change)).grid(
        row=drinksRowsCount + 3, column=0)


def enterSum(value):
    global enteredSum
    enteredSum += value
    updateLabels()


# all widgets will be here
# Execute Tkinter
root.mainloop()
