import tkinter as tk
from tkinter import Button, Entry, Label, messagebox
import csv
import os

class AdminPanel:
    def __init__(self, root, stock_manager, price_calculator, update_ui_callback):
        """
        Initializes the AdminPanel class which allows the user to manage products,
        update stock levels, and set prices. It also provides an interface for 
        dynamically adding new products.

        :param root: The Tkinter root window (admin window).
        :param stock_manager: Instance of the Stock class to manage stock data.
        :param price_calculator: Instance of the PriceCalculator class to manage product prices.
        :param update_ui_callback: Callback function to update the UI when changes are made.
        """
        self.root = root
        self.stock_manager = stock_manager
        self.price_calculator = price_calculator
        self.update_ui_callback = update_ui_callback  # Callback for UI update

        # Frame for displaying existing products
        self.products_frame = tk.Frame(root)
        self.products_frame.pack()

        # Frame for adding new products
        self.new_product_frame = tk.Frame(root)
        self.new_product_frame.pack(pady=10)

        # Load and display the existing products
        self.load_products()
        # Display the section to add a new product
        self.add_new_product_section()

    def load_products(self):
        """
        Loads the products from stock and displays each product with its current stock level.
        Provides buttons to increase/decrease stock or remove a product.
        """
        # Remove old widgets before reloading products
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        # Column headers
        Label(self.products_frame, text="Product", width=20).grid(row=0, column=0)
        Label(self.products_frame, text="Stock", width=10).grid(row=0, column=1)
        Label(self.products_frame, text="Actions", width=20).grid(row=0, column=2)

        # Display all products with stock levels and action buttons
        for idx, (product_name, quantity) in enumerate(self.stock_manager.stock_data.items(), start=1):
            # Get the product price
            price = self.price_calculator.get_price(product_name)
            Label(self.products_frame, text=f"{product_name} - {price:.2f} €", width=20).grid(row=idx, column=0)
            Label(self.products_frame, text=str(quantity), width=10).grid(row=idx, column=1)

            # Buttons to increase or decrease stock and remove the product
            Button(self.products_frame, text="+", command=lambda p=product_name: self.update_stock(p, 1)).grid(row=idx, column=2)
            Button(self.products_frame, text="-", command=lambda p=product_name: self.update_stock(p, -1)).grid(row=idx, column=3)
            Button(self.products_frame, text="Remove", command=lambda p=product_name: self.remove_product(p)).grid(row=idx, column=4)

    def update_stock(self, product_name, amount):
        """
        Updates the stock level of a specific product by increasing or decreasing the quantity.

        :param product_name: The name of the product to update.
        :param amount: The amount to adjust the stock by (positive or negative).
        """
        if product_name in self.stock_manager.stock_data:
            # Update the stock quantity
            self.stock_manager.stock_data[product_name] += amount
            if self.stock_manager.stock_data[product_name] < 0:
                self.stock_manager.stock_data[product_name] = 0  # Ensure stock doesn't go below 0
            self.save_stock()  # Save updated stock data to CSV
            self.load_products()  # Reload the products to reflect changes

    def remove_product(self, product_name):
        """
        Removes a product from both the stock and price data after confirming with the user.

        :param product_name: The name of the product to remove.
        """
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove {product_name}?"):
            # Remove the product from stock and price data
            del self.stock_manager.stock_data[product_name]
            del self.price_calculator.prices_data[product_name]
            self.save_stock()  # Save updated stock data to CSV
            self.save_prices()  # Save updated price data to CSV
            self.load_products()  # Reload the products to reflect changes

    def add_new_product_section(self):
        """
        Displays the section in the admin panel where users can add a new product
        with an initial quantity and price.
        """
        # Product name input
        Label(self.new_product_frame, text="New Product:").grid(row=0, column=0)
        self.new_product_name = Entry(self.new_product_frame)
        self.new_product_name.grid(row=0, column=1)

        # Initial stock with increment/decrement buttons
        Label(self.new_product_frame, text="Initial Stock:").grid(row=0, column=2)
        self.new_product_quantity = tk.IntVar(value=0)  # Variable to hold stock quantity
        Label(self.new_product_frame, textvariable=self.new_product_quantity).grid(row=0, column=3)
        Button(self.new_product_frame, text="+", command=lambda: self.update_new_product_quantity(1)).grid(row=0, column=4)
        Button(self.new_product_frame, text="-", command=lambda: self.update_new_product_quantity(-1)).grid(row=0, column=5)

        # Price control with increment/decrement buttons
        Label(self.new_product_frame, text="Price (€):").grid(row=1, column=0)
        self.new_product_price = tk.DoubleVar(value=0.0)  # Variable to hold product price
        Label(self.new_product_frame, textvariable=self.new_product_price).grid(row=1, column=1)
        Button(self.new_product_frame, text="+", command=lambda: self.update_new_product_price(0.1)).grid(row=1, column=2)
        Button(self.new_product_frame, text="-", command=lambda: self.update_new_product_price(-0.1)).grid(row=1, column=3)

        # Button to add the new product
        Button(self.new_product_frame, text="Add", command=self.add_product).grid(row=1, column=4)

    def update_new_product_quantity(self, amount):
        """
        Updates the quantity of the new product being added.

        :param amount: The amount to adjust the quantity by (positive or negative).
        """
        current_quantity = self.new_product_quantity.get()
        new_quantity = max(0, current_quantity + amount)  # Quantity should not be negative
        self.new_product_quantity.set(new_quantity)

    def update_new_product_price(self, amount):
        """
        Updates the price of the new product being added.

        :param amount: The amount to adjust the price by (positive or negative).
        """
        current_price = self.new_product_price.get()
        new_price = max(0.0, round(current_price + amount, 2))  # Price should not be negative, round to 2 decimal places
        self.new_product_price.set(new_price)

    def add_product(self):
        """
        Adds a new product to the stock and price list based on user input.
        Validates the product name, quantity, and price before adding the product.
        """
        name = self.new_product_name.get().strip()  # Get and clean the product name
        quantity = self.new_product_quantity.get()  # Get the initial stock quantity
        price = self.new_product_price.get()  # Get the product price

        # Validate product name
        if not name:
            messagebox.showerror("Error", "Invalid product name.")
            return

        # Check if the product already exists
        if name in self.stock_manager.stock_data:
            messagebox.showerror("Error", "Product already exists.")
            return

        # Add the new product to stock and price data
        self.stock_manager.stock_data[name] = quantity  # Save the product quantity
        self.price_calculator.prices_data[name] = price  # Save the product price
        self.save_stock()  # Save updated stock data to CSV
        self.save_prices()  # Save updated price data to CSV
        self.load_products()  # Reload the products to reflect changes

        # Update the customer-facing UI to show the new product
        self.update_ui_callback()

    def save_stock(self):
        """
        Saves the current stock data to the stock.csv file.
        """
        # Corrected path to stock.csv
        stock_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Backend', 'CSV', 'stock.csv')
        with open(stock_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "quantity"])  # Write headers
            for name, quantity in self.stock_manager.stock_data.items():
                writer.writerow([name, quantity])  # Write each product and its quantity

    def save_prices(self):
        """
        Saves the current price data to the prices.csv file.
        """
        # Corrected path to prices.csv
        prices_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Backend', 'CSV', 'prices.csv')
        with open(prices_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["name", "price"])  # Write headers
            for name, price in self.price_calculator.prices_data.items():
                writer.writerow([name, price])  # Write each product and its price