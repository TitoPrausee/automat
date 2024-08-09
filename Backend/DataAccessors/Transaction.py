import csv
import os

class Transaction:
    dirname = os.path.dirname(os.path.dirname(__file__))
    csvPath = os.path.join(dirname, 'CSV/transactions.csv')

    @staticmethod
    def Save(item):
        with open(Transaction.csvPath, 'a', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, ['item'])
            writer.writerow({'item': item } )