# CSVHandler.py

import csv

class CSVHandler:

    def read_csv(self, file_path):
        data = {}
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'price' in row:
                    data[row['name']] = float(row['price'])
                elif 'quantity' in row:
                    data[row['name']] = int(row['quantity'])
        return data

    def write_csv(self, file_path, data):
        with open(file_path, mode='w', newline='') as file:
            if all(isinstance(value, float) for value in data.values()):
                writer = csv.DictWriter(file, fieldnames=['name', 'price'])
                writer.writeheader()
                for name, price in data.items():
                    writer.writerow({'name': name, 'price': price})
            else:
                writer = csv.DictWriter(file, fieldnames=['name', 'quantity'])
                writer.writeheader()
                for name, quantity in data.items():
                    writer.writerow({'name': name, 'quantity': quantity})