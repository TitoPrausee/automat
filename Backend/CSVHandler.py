import csv
import os
import os.path


def CreateIfMissing(filedescriptions):
        dirname = os.path.dirname(__file__)
        for file in filedescriptions:
                fullpath = os.path.join(dirname, 'CSV/' + file[0])
                if os.path.isfile(fullpath) is False:
                        with open(fullpath, 'w', newline='') as csvFile:
                                fieldnames = file[1]

                                writer = csv.DictWriter(csvFile, fieldnames)
                                writer.writeheader()

def DeleteCSVs(filenames):
        dirname = os.path.dirname(__file__)
        for file in filenames:
                fullpath = os.path.join(dirname, 'CSV/' + file)
                os.remove(fullpath)

DeleteCSVs(['prices.csv', 'transactions.csv', 'stock.csv'])
CreateIfMissing([('prices.csv', ['item', 'price']), ('transactions.csv', ['item']), ('stock.csv', ['item', 'quantity'])])