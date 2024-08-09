import csv
import os

class Price:
    _dirname = os.path.dirname(os.path.dirname(__file__))
    _csvPath = os.path.join(_dirname, 'CSV/price.csv')
    
    @staticmethod
    def readAllPrices(): 
        pricesData = {}
        with open(Price.csvPath, "r", newline='') as csvFile:
            reader = csv.DictReader(csvFile)
            for row in reader:
                pricesData[row['name']] = float(row['price'])

        return pricesData
    
    @staticmethod
    def updatePrice(name, price):
        #read all data
        if os.path.isfile(Price._csvPath) is False:
            return
        
        with open(Price._csvPath, "r", newline='') as csvFile:
            reader = csv.DictReader(csvFile)
            priceData = list(reader)

        priceDict = {item['name']: float(item['price']) for item in priceData}

        #update the data
        if name in priceDict:
            priceDict[name] = price

        updatedPriceData = [{'name': name, 'quantity': price} for name, price in priceDict.items()]

        #save the data
        with open (Price._csvPath, "w", newline='') as csvFile:
            fieldnames = ['name', 'price']
            writer = csv.DictWriter(csvFile, fieldnames)
            writer.writeheader()
            for item in updatedPriceData:
                writer.writerow(item)