import csv
import os

class Stock:
    dirname = os.path.dirname(os.path.dirname(__file__))
    csvPath = os.path.join(dirname, 'CSV/stock.csv')
    fieldnames = ['item', 'quantity']

    @staticmethod
    def update_stock(updates):    
        # Read the existing stock data
        stock_data = []
        if os.path.isfile(Stock.csvPath):
            with open(Stock.csvPath, mode='r', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                stock_data = list(reader)
    
        # Convert stock_data to a dictionary for easy updates
        stock_dict = {item['name']: int(item['quantity']) for item in stock_data}
    
        # Apply the updates
        for item, change in updates.items():
            if item in stock_dict:
                stock_dict[item] += change
            else:
                stock_dict[item] = change
    
        # Convert the dictionary back to a list of dictionaries
        updated_stock_data = [{'name': name, 'quantity': quantity} for name, quantity in stock_dict.items()]
    
        # Write the updated stock data back to the CSV file
        with open(Stock.csvPath, mode='w', newline='') as csvfile:
            fieldnames = ['name', 'quantity']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in updated_stock_data:
                writer.writerow(item)    

#stock = Stock()
#updates = {'Cola': -5}
#stock.update_stock(updates)