import csv
import os

class Transaction:
    dirname = os.path.dirname(os.path.dirname(__file__))
    csvPath = os.path.join(dirname, 'CSV/transactions.csv')

    def Save(self, item):
        with open(self.csvPath, 'a', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, ['item'])
            writer.writerow({'item': item } )