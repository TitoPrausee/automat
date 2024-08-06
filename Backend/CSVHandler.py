import csv
import os
import os.path

def CreateIfMissing(filenames):
        dirname = os.path.dirname(__file__)
        for file in filenames:
                fullpath = os.path.join(dirname, 'CSV/' + file[0])
                if os.path.isfile(fullpath) is False:
                        with open(fullpath, 'w', newline='') as csvFile:
                                fieldnames = file[1]
                                writer = csv.DictWriter(csvFile, fieldnames)
                                writer.writeheader()

                            
CreateIfMissing([('prices.csv', ['name', 'price']), ('transactions.csv', ['Id', 'item'])])