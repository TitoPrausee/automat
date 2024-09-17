import tkinter as tk
from tkinter import Button, Entry, Label, messagebox
import csv
import os

class AdminPanel:
    def __init__(self, root, stock_manager, price_calculator, update_ui_callback):
        self.root = root
        self.stock_manager = stock_manager
        self.price_calculator = price_calculator
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

        # Zeigt alle Produkte an
        for idx, (product_name, quantity) in enumerate(self.stock_manager.stock_data.items(), start=1):
            price = self.price_calculator.get_price(product_name)
            Label(self.products_frame, text=f"{product_name} - {price:.2f} €", width=20).grid(row=idx, column=0)
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
            del self.price_calculator.prices_data[product_name]
            self.save_stock()
            self.save_prices()
            self.load_products()

    def add_new_product_section(self):
        Label(self.new_product_frame, text="Neues Produkt:").grid(row=0, column=0)
        self.new_product_name = Entry(self.new_product_frame)
        self.new_product_name.grid(row=0, column=1)

        # Anfangsbestand mit Buttons für + und -
        Label(self.new_product_frame, text="Anfangsbestand:").grid(row=0, column=2)
        self.new_product_quantity = tk.IntVar(value=0)  # Mengenvariable
        Label(self.new_product_frame, textvariable=self.new_product_quantity).grid(row=0, column=3)
        Button(self.new_product_frame, text="+", command=lambda: self.update_new_product_quantity(1)).grid(row=0, column=4)
        Button(self.new_product_frame, text="-", command=lambda: self.update_new_product_quantity(-1)).grid(row=0, column=5)

        # Preissteuerung mit + und - Buttons
        Label(self.new_product_frame, text="Preis (€):").grid(row=1, column=0)
        self.new_product_price = tk.DoubleVar(value=0.0)  # Preisvariable
        Label(self.new_product_frame, textvariable=self.new_product_price).grid(row=1, column=1)
        Button(self.new_product_frame, text="+", command=lambda: self.update_new_product_price(0.1)).grid(row=1, column=2)
        Button(self.new_product_frame, text="-", command=lambda: self.update_new_product_price(-0.1)).grid(row=1, column=3)

        Button(self.new_product_frame, text="Hinzufügen", command=self.add_product).grid(row=1, column=4)

    def update_new_product_quantity(self, amount):
        current_quantity = self.new_product_quantity.get()
        new_quantity = max(0, current_quantity + amount)  # Menge darf nicht negativ sein
        self.new_product_quantity.set(new_quantity)

    def update_new_product_price(self, amount):
        current_price = self.new_product_price.get()
        new_price = max(0.0, round(current_price + amount, 2))  # Preis darf nicht negativ sein, runde auf 2 Dezimalstellen
        self.new_product_price.set(new_price)

    def add_product(self):
        name = self.new_product_name.get().strip()
        quantity = self.new_product_quantity.get()
        price = self.new_product_price.get()

        if not name:
            messagebox.showerror("Fehler", "Ungültiger Name.")
            return

        if name in self.stock_manager.stock_data:
            messagebox.showerror("Fehler", "Produkt existiert bereits.")
            return

        # Füge das neue Produkt hinzu
        self.stock_manager.stock_data[name] = quantity  # Menge speichern
        self.price_calculator.prices_data[name] = price  # Preis speichern
        self.save_stock()
        self.save_prices()
        self.load_products()

        # UI der Kundenschnittstelle aktualisieren
        self.update_ui_callback()

    def save_stock(self):
        # Korrigierter Pfad zur stock.csv
        stock_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Backend', 'CSV', 'stock.csv')
        with open(stock_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "quantity"])
            for name, quantity in self.stock_manager.stock_data.items():
                writer.writerow([name, quantity])

    def save_prices(self):
        # Korrigierter Pfad zur prices.csv
        prices_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Backend', 'CSV', 'prices.csv')
        with open(prices_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "price"])
            for name, price in self.price_calculator.prices_data.items():
                writer.writerow([name, price])