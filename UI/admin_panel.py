import tkinter as tk
from tkinter import Button, Entry, Label, messagebox
import csv
import os

class AdminPanel:
    """
    Stellt das Admin-Panel dar, mit dem der Benutzer Produkte verwalten,
    Lagerbestände aktualisieren und Preise festlegen kann. Es bietet auch eine
    Oberfläche zum dynamischen Hinzufügen neuer Produkte.

    :param root: Das Tkinter-Stammfenster (Admin-Fenster).
    :param stock_manager: Instanz der Stock-Klasse zur Verwaltung der Lagerdaten.
    :param price_calculator: Instanz der PriceCalculator-Klasse zur Verwaltung der Produktpreise.
    :param update_ui_callback: Rückruffunktion zum Aktualisieren der Benutzeroberfläche, wenn Änderungen vorgenommen werden.
    """
    def __init__(self, root, stock_manager, price_calculator, update_ui_callback):
        self.root = root
        self.stock_manager = stock_manager
        self.price_calculator = price_calculator
        self.update_ui_callback = update_ui_callback  # Rückruf für UI-Aktualisierung

        # Frame zur Anzeige vorhandener Produkte
        self.products_frame = tk.Frame(root)
        self.products_frame.pack()

        # Frame zum Hinzufügen neuer Produkte
        self.new_product_frame = tk.Frame(root)
        self.new_product_frame.pack(pady=10)

        # Laden und Anzeigen der vorhandenen Produkte
        self.load_products()
        # Anzeigen des Abschnitts zum Hinzufügen eines neuen Produkts
        self.add_new_product_section()

    def load_products(self):
        """
        Lädt die Produkte aus dem Lager und zeigt jedes Produkt mit seinem aktuellen Lagerbestand an.
        Stellt Schaltflächen zum Erhöhen/Verringern des Lagerbestands oder zum Entfernen eines Produkts bereit.
        """
        # Alte Widgets entfernen, bevor Produkte neu geladen werden
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        # Spaltenüberschriften
        Label(self.products_frame, text="Produkt", width=20).grid(row=0, column=0)
        Label(self.products_frame, text="Lagerbestand", width=10).grid(row=0, column=1)
        Label(self.products_frame, text="Aktionen", width=20).grid(row=0, column=2)

        # Alle Produkte mit Lagerbeständen und Aktionsschaltflächen anzeigen
        for idx, (product_name, quantity) in enumerate(self.stock_manager.stock_data.items(), start=1):
            # Produktpreis abrufen
            price = self.price_calculator.get_price(product_name)
            Label(self.products_frame, text=f"{product_name} - {price:.2f} €", width=20).grid(row=idx, column=0)
            Label(self.products_frame, text=str(quantity), width=10).grid(row=idx, column=1)

            # Schaltflächen zum Erhöhen oder Verringern des Lagerbestands und zum Entfernen des Produkts
            Button(self.products_frame, text="+", command=lambda p=product_name: self.update_stock(p, 1)).grid(row=idx, column=2)
            Button(self.products_frame, text="-", command=lambda p=product_name: self.update_stock(p, -1)).grid(row=idx, column=3)
            Button(self.products_frame, text="Entfernen", command=lambda p=product_name: self.remove_product(p)).grid(row=idx, column=4)

    def update_stock(self, product_name, amount):
        """
        Aktualisiert den Lagerbestand eines bestimmten Produkts durch Erhöhen oder Verringern der Menge.

        :param product_name: Der Name des zu aktualisierenden Produkts.
        :param amount: Der Betrag, um den der Lagerbestand angepasst werden soll (positiv oder negativ).
        """
        if product_name in self.stock_manager.stock_data:
            # Lagermenge aktualisieren
            self.stock_manager.stock_data[product_name] += amount
            if self.stock_manager.stock_data[product_name] < 0:
                self.stock_manager.stock_data[product_name] = 0  # Sicherstellen, dass der Lagerbestand nicht unter 0 fällt
            self.save_stock()  # Aktualisierte Lagerdaten in CSV speichern
            self.load_products()  # Produkte neu laden, um Änderungen widerzuspiegeln

    def remove_product(self, product_name):
        """
        Entfernt ein Produkt aus den Lager- und Preisdaten, nachdem der Benutzer dies bestätigt hat.

        :param product_name: Der Name des zu entfernenden Produkts.
        """
        if messagebox.askyesno("Bestätigen", f"Möchten Sie {product_name} wirklich entfernen?"):
            # Produkt aus Lager- und Preisdaten entfernen
            del self.stock_manager.stock_data[product_name]
            del self.price_calculator.prices_data[product_name]
            self.save_stock()  # Aktualisierte Lagerdaten in CSV speichern
            self.save_prices()  # Aktualisierte Preisdaten in CSV speichern
            self.load_products()  # Produkte neu laden, um Änderungen widerzuspiegeln

    def add_new_product_section(self):
        """
        Zeigt den Abschnitt im Admin-Panel an, in dem Benutzer ein neues Produkt
        mit einer Anfangsmenge und einem Preis hinzufügen können.
        """
        # Eingabe des Produktnamens
        Label(self.new_product_frame, text="Neues Produkt:").grid(row=0, column=0)
        self.new_product_name = Entry(self.new_product_frame)
        self.new_product_name.grid(row=0, column=1)

        # Anfangsbestand mit Schaltflächen zum Erhöhen/Verringern
        Label(self.new_product_frame, text="Anfangsbestand:").grid(row=0, column=2)
        self.new_product_quantity = tk.IntVar(value=0)  # Variable zum Speichern der Lagermenge
        Label(self.new_product_frame, textvariable=self.new_product_quantity).grid(row=0, column=3)
        Button(self.new_product_frame, text="+", command=lambda: self.update_new_product_quantity(1)).grid(row=0, column=4)
        Button(self.new_product_frame, text="-", command=lambda: self.update_new_product_quantity(-1)).grid(row=0, column=5)

        # Preissteuerung mit Schaltflächen zum Erhöhen/Verringern
        Label(self.new_product_frame, text="Preis (€):").grid(row=1, column=0)
        self.new_product_price = tk.DoubleVar(value=0.0)  # Variable zum Speichern des Produktpreises
        Label(self.new_product_frame, textvariable=self.new_product_price).grid(row=1, column=1)
        Button(self.new_product_frame, text="+", command=lambda: self.update_new_product_price(0.1)).grid(row=1, column=2)
        Button(self.new_product_frame, text="-", command=lambda: self.update_new_product_price(-0.1)).grid(row=1, column=3)

        # Schaltfläche zum Hinzufügen des neuen Produkts
        Button(self.new_product_frame, text="Hinzufügen", command=self.add_product).grid(row=1, column=4)

    def update_new_product_quantity(self, amount):
        """
        Aktualisiert die Menge des neuen Produkts, das hinzugefügt wird.

        :param amount: Der Betrag, um den die Menge angepasst werden soll (positiv oder negativ).
        """
        current_quantity = self.new_product_quantity.get()
        new_quantity = max(0, current_quantity + amount)  # Menge sollte nicht negativ sein
        self.new_product_quantity.set(new_quantity)

    def update_new_product_price(self, amount):
        """
        Aktualisiert den Preis des neuen Produkts, das hinzugefügt wird.

        :param amount: Der Betrag, um den der Preis angepasst werden soll (positiv oder negativ).
        """
        current_price = self.new_product_price.get()
        new_price = max(0.0, round(current_price + amount, 2))  # Preis sollte nicht negativ sein, auf 2 Dezimalstellen runden
        self.new_product_price.set(new_price)

    def add_product(self):
        """
        Fügt ein neues Produkt zur Lager- und Preisliste basierend auf Benutzereingaben hinzu.
        Validiert den Produktnamen, die Menge und den Preis, bevor das Produkt hinzugefügt wird.
        """
        name = self.new_product_name.get().strip()  # Produktnamen abrufen und bereinigen
        quantity = self.new_product_quantity.get()  # Anfangsbestand abrufen
        price = self.new_product_price.get()  # Produktpreis abrufen

        # Produktnamen validieren
        if not name:
            messagebox.showerror("Fehler", "Ungültiger Produktname.")
            return

        # Prüfen, ob das Produkt bereits existiert
        if name in self.stock_manager.stock_data:
            messagebox.showerror("Fehler", "Produkt existiert bereits.")
            return

        # Neues Produkt zu Lager- und Preisdaten hinzufügen
        self.stock_manager.stock_data[name] = quantity  # Produktmenge speichern
        self.price_calculator.prices_data[name] = price  # Produktpreis speichern
        self.save_stock()  # Aktualisierte Lagerdaten in CSV speichern
        self.save_prices()  # Aktualisierte Preisdaten in CSV speichern
        self.load_products()  # Produkte neu laden, um Änderungen widerzuspiegeln

        # Kundenbezogene Benutzeroberfläche aktualisieren, um das neue Produkt anzuzeigen
        self.update_ui_callback()

    def save_stock(self):
        """
        Speichert die aktuellen Lagerdaten in der Datei stock.csv.
        """
        # Korrigierter Pfad zu stock.csv
        stock_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Backend', 'CSV', 'stock.csv')
        with open(stock_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "quantity"])  # Überschriften schreiben
            for name, quantity in self.stock_manager.stock_data.items():
                writer.writerow([name, quantity])  # Jedes Produkt und seine Menge schreiben

    def save_prices(self):
        """
        Speichert die aktuellen Preisdaten in der Datei prices.csv.
        """
        # Korrigierter Pfad zu prices.csv
        prices_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Backend', 'CSV', 'prices.csv')
        with open(prices_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "price"])  # Überschriften schreiben
            for name, price in self.price_calculator.prices_data.items():
                writer.writerow([name, price])  # Jedes Produkt und seinen Preis schreiben