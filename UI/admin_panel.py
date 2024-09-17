import tkinter as tk
from tkinter import Button, Entry, Label, messagebox
import csv
import os

class AdminPanel:
    def __init__(self, root, stock_manager, update_ui_callback):
        self.root = root
        self.stock_manager = stock_manager
        self.update_ui_callback = update_ui_callback  # Callback für UI-Aktualisierung

        self.products_frame = tk.Frame(root)
        self.products_frame.pack()

        self.new_product_frame = tk.Frame(root)
        self.new_product_frame.pack(pady=10)

        self.load_products()
        self.add_new_product_section()

    def load_products(self):
        # Entfernt alte Widgets
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        # Titelzeile
        Label(self.products_frame, text="Produkt", width=20).grid(row=0, column=0)
        Label(self.products_frame, text="Bestand", width=10).grid(row=0, column=1)
        Label(self.products_frame, text="Aktionen", width=20).grid(row=0, column=2)

        # Definiere die Standardprodukte (falls diese nicht schon in der CSV-Datei sind)
        standard_products = {
            "Cola": 0,
            "Sprite": 0,
            "Fanta": 0,
            "Wasser": 0,
            "Eistee": 0
        }

        # Mische Standardprodukte mit dem aktuellen Lagerbestand
        all_products = {**standard_products, **self.stock_manager.stock_data}

        # Zeigt alle Produkte an, auch wenn sie leer sind
        for idx, (product_name, quantity) in enumerate(all_products.items(), start=1):
            Label(self.products_frame, text=product_name, width=20).grid(row=idx, column=0)
            Label(self.products_frame, text=str(quantity), width=10).grid(row=idx, column=1)

            Button(self.products_frame, text="+", command=lambda p=product_name: self.update_stock(p, 1)).grid(row=idx, column=2)
            Button(self.products_frame, text="-", command=lambda p=product_name: self.update_stock(p, -1)).grid(row=idx, column=3)
            Button(self.products_frame, text="Entfernen", command=lambda p=product_name: self.remove_product(p)).grid(row=idx, column=4)

    def update_stock(self, product_name, amount):
        if product_name in self.stock_manager.stock_data:
            self.stock_manager.stock_data[product_name] += amount
            if self.stock_manager.stock_data[product_name] < 0:
                self.stock_manager.stock_data[product_name] = 0
            self.save_stock()
            self.load_products()

    def remove_product(self, product_name):
        if messagebox.askyesno("Bestätigen", f"Willst du {product_name} wirklich entfernen?"):
            del self.stock_manager.stock_data[product_name]
            self.save_stock()
            self.load_products()

    def add_new_product_section(self):
        Label(self.new_product_frame, text="Neues Produkt:").grid(row=0, column=0)
        self.new_product_name = Entry(self.new_product_frame)
        self.new_product_name.grid(row=0, column=1)
        
        Label(self.new_product_frame, text="Anfangsbestand:").grid(row=0, column=2)
        self.new_product_quantity = Entry(self.new_product_frame)
        self.new_product_quantity.grid(row=0, column=3)

        Button(self.new_product_frame, text="Hinzufügen", command=self.add_product).grid(row=0, column=4)

    def add_product(self):
        name = self.new_product_name.get().strip()
        quantity = self.new_product_quantity.get().strip()
        if not name or not quantity.isdigit():
            messagebox.showerror("Fehler", "Ungültiger Name oder Bestand.")
            return

        if name in self.stock_manager.stock_data:
            messagebox.showerror("Fehler", "Produkt existiert bereits.")
            return

        self.stock_manager.stock_data[name] = int(quantity)
        self.save_stock()
        self.load_products()

        # UI der Kundenschnittstelle aktualisieren
        self.update_ui_callback()  # Hier wird die Hauptansicht aktualisiert

    def save_stock(self):
        # Korrigierter Pfad zur stock.csv
        stock_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Backend', 'CSV', 'stock.csv')
        with open(stock_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "quantity"])
            for name, quantity in self.stock_manager.stock_data.items():
                writer.writerow([name, quantity])

# Integration des Admin-Panels in die Anwendung
if __name__ == "__main__":
    from Backend.DataAccessors.Stock import Stock
    from Backend.CSVHandler import CSVHandler

    root = tk.Tk()
    root.title("Admin Panel")

    # Beispielhafter StockManager
    csv_handler = CSVHandler()
    stock_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Backend', 'CSV', 'stock.csv')
    stock_manager = Stock(csv_handler, stock_file_path)

    app = AdminPanel(root, stock_manager, update_ui_callback=lambda: print("UI aktualisieren"))  # Dummy-Callback für Test
    root.mainloop()