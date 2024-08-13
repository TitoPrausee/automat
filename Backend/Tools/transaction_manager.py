"""
Transaction Management
=======================
Handles the transaction process including product selection, payment,
stock management, transaction logging, and change processing.
"""

# 1. Klasse zur Verwaltung von Transaktionen
class TransactionManager:
    """
    Manages a transaction including product selection, payment processing,
    stock updates, and transaction logging.

    Attributes:
        price_calculator: Function to calculate the total price of selected products.
        stock_manager: Object to manage stock-related operations.
        transaction_logger: Object to log transaction details.
        banknotes_manager: Object to manage banknote-related operations.
        selected_product: Stores details of the currently selected product.
        entered_sum: Accumulates the total amount of money entered by the user.
    """

    # 1.1 Konstruktor der Klasse
    def __init__(self, price_calculator, stock_manager, transaction_logger, banknotes_manager):
        """
        Initialize the TransactionManager with required managers and utilities.
        
        :param price_calculator: Function to calculate the total price of selected products.
        :param stock_manager: Object to manage stock-related operations.
        :param transaction_logger: Object to log transaction details.
        :param banknotes_manager: Object to manage banknote-related operations.
        """
        self.price_calculator = price_calculator  # Kalkuliert Preise der ausgewählten Produkte
        self.stock_manager = stock_manager  # Verwalten von Lagerbeständen
        self.transaction_logger = transaction_logger  # Loggt Transaktionsdetails
        self.banknotes_manager = banknotes_manager  # Verwalten von Banknoten
        self.selected_product = None  # Speichert Details des ausgewählten Produkts
        self.entered_sum = 0  # Akkumulierte Summe des eingegebenen Betrags

    # 1.2 Produkt auswählen
    def select_product(self, product_name, quantity=1):
        """
        Select a product and store its price and details after checking stock availability.

        :param product_name: Name of the product selected.
        :param quantity: Number of units of the product selected.
        :return: True if the product is selected successfully, else False.
        """
        if not self.stock_manager.is_in_stock(product_name, quantity):
            print(f"Das Produkt {product_name} ist ausverkauft oder die gewünschte Menge ist nicht verfügbar.")
            return False

        total_price = self.price_calculator.calculate_total_price(product_name, quantity)
        self.selected_product = {
            'name': product_name,
            'quantity': quantity,
            'total_price': total_price
        }
        print(f"Produkt gewählt: {product_name}, Menge: {quantity}, Preis: {total_price:.2f} €")
        return True

    # 1.3 Geldbetrag eingeben
    def enter_money(self, amount):
        """
        Enter a monetary amount and add it to the current total entered sum.

        :param amount: The amount of money being entered by the user.
        """
        if self.selected_product:
            self.entered_sum += amount  # Betrag zur aktuellen Summe hinzufügen
            print(f"Eingegebener Betrag: {self.entered_sum:.2f} €")
        else:
            print("Es wurde kein Produkt ausgewählt.")

    # 1.4 Zahlung prüfen
    def check_payment(self):
        """
        Check if the entered amount is sufficient for the selected product.

        :return: True if payment is sufficient, otherwise False.
        """
        if self.entered_sum >= self.selected_product['total_price']:
            print("Zahlung erfolgreich.")
            return True
        else:
            remaining = self.selected_product['total_price'] - self.entered_sum
            print(f"Nicht genug Geld. Noch zu zahlen: {remaining:.2f} €")
            return False

    # 1.5 Wechselgeld berechnen und ausgeben
    def process_change(self):
        """
        Process and return change if necessary.

        :return: The amount of change to be returned.
        """
        change = self.entered_sum - self.selected_product['total_price']
        if change > 0:
            change_banknotes = self.banknotes_manager.sumToBanknotes(change)
            formatted_change = self.banknotes_manager.formatBanknotes(change_banknotes)
            print(f"Wechselgeld: {formatted_change}")
        else:
            print("Kein Wechselgeld nötig.")
        return change

    # 1.6 Transaktion abschließen
    def finalize_transaction(self):
        """
        Finalize the transaction: check payment, process change, update stock,
        log the transaction, and reset the transaction.
        """
        if self.selected_product is None:
            print("Keine Transaktion durchführbar. Produkt nicht verfügbar.")
            return

        if self.check_payment():
            self.process_change()
            self.stock_manager.update_stock({self.selected_product['name']: -self.selected_product['quantity']})
            self.transaction_logger.Save(self.selected_product['name'])
            print(f"Produkt {self.selected_product['name']} ausgegeben.")
            self.reset_transaction()
        else:
            print("Transaktion fehlgeschlagen. Bitte mehr Geld eingeben.")

    # 1.7 Transaktion zurücksetzen
    def reset_transaction(self):
        """
        Reset the transaction by clearing the selected product and entered sum.
        """
        self.selected_product = None  # Ausgewähltes Produkt zurücksetzen
        self.entered_sum = 0  # Eingegebene Summe zurücksetzen


"""
Stock Management
=================
Handles loading, saving, and managing stock levels of products.
"""

# 2. Klasse zur Verwaltung des Lagerbestands
class Stock:
    """
    Manages the stock of products, including importing from and exporting to CSV files.

    Attributes:
        csv_handler: Object to handle CSV reading and writing.
        stock_file: The file name of the stock CSV.
        stock_data: Dictionary holding the current stock data.
    """

    # 2.1 Konstruktor der Klasse
    def __init__(self, csv_handler, stock_file):
        """
        Initialize the Stock manager with a CSV handler and stock file.

        :param csv_handler: Object responsible for reading and writing CSV files.
        :param stock_file: The CSV file to load and save stock data.
        """
        self.csv_handler = csv_handler  # Handler für CSV-Operationen
        self.stock_file = stock_file  # Pfad zur Lagerbestandsdatei
        self.stock_data = self.load_stock_from_csv()  # Lädt Lagerdaten beim Initialisieren

    # 2.2 Lagerbestand aus CSV-Datei laden
    def load_stock_from_csv(self):
        """
        Load stock data from a CSV file into the stock_data dictionary.

        :return: A dictionary of stock items and their quantities.
        """
        data = self.csv_handler.read_csv(self.stock_file)
        return {row['item']: int(row['quantity']) for row in data}

    # 2.3 Lagerbestand aktualisieren
    def update_stock(self, updates):
        """
        Update the stock based on the provided updates.

        :param updates: A dictionary where keys are item names and values are the quantity changes.
        """
        for item, change in updates.items():
            if item in self.stock_data:
                self.stock_data[item] += change  # Vorhandene Menge aktualisieren
            else:
                self.stock_data[item] = change  # Neues Produkt hinzufügen
        self.save_stock_to_csv()

    # 2.4 Überprüfen, ob ein Produkt in ausreichender Menge auf Lager ist
    def is_in_stock(self, item_name, quantity):
        """
        Check if the item is in stock and if the requested quantity is available.
        
        :param item_name: Name of the item to check.
        :param quantity: Desired quantity of the item.
        :return: True if the item is in stock and the quantity is available, else False.
        """
        return self.stock_data.get(item_name, 0) >= quantity

    # 2.5 Lagerbestand in CSV-Datei speichern
    def save_stock_to_csv(self):
        """
        Save the current stock data to a CSV file.
        """
        updated_stock_data = [{'item': name, 'quantity': quantity} for name, quantity in self.stock_data.items()]
        self.csv_handler.write_csv(self.stock_file, updated_stock_data)
