# Transaction Management
# =======================
# Handles the transaction process including product selection, payment,
# stock management, transaction logging, and change processing.

from Backend.DataAccessors.Stock import Stock  # Verwende die Stock-Klasse aus stock_handler.py

class TransactionManager:
    """
    Manages a transaction including product selection, payment processing,
    stock updates, and transaction logging.
    """

    def __init__(self, price_calculator, stock_manager, transaction_logger, banknotes_manager):
        """
        Initialize the TransactionManager with required managers and utilities.
        """
        self.price_calculator = price_calculator  # Kalkuliert Preise der ausgewählten Produkte
        self.stock_manager = stock_manager  # Verwalten von Lagerbeständen
        self.transaction_logger = transaction_logger  # Loggt Transaktionsdetails
        self.banknotes_manager = banknotes_manager  # Verwalten von Banknoten
        self.selected_product = None  # Speichert Details des ausgewählten Produkts
        self.entered_sum = 0  # Akkumulierte Summe des eingegebenen Betrags

    def select_product(self, product_name, quantity=1):
        """
        Select a product and store its price and details after checking stock availability.
        """
        if not self.stock_manager.is_in_stock(product_name, quantity):
            print(f"Das Produkt {product_name} ist ausverkauft oder die gewünschte Menge ist nicht verfügbar.")
            return False

        total_price = self.price_calculator.get_price(product_name) * quantity  # Preis mit PriceCalculator berechnen
        self.selected_product = {
            'name': product_name,
            'quantity': quantity,
            'total_price': total_price
        }
        print(f"Produkt gewählt: {product_name}, Menge: {quantity}, Preis: {total_price:.2f} €")
        return True

    def enter_money(self, amount):
        """
        Enter a monetary amount and add it to the current total entered sum.
        """
        if self.selected_product:
            self.entered_sum += amount
            print(f"Eingegebener Betrag: {self.entered_sum:.2f} €")
        else:
            print("Es wurde kein Produkt ausgewählt.")

    def check_payment(self):
        """
        Check if the entered amount is sufficient for the selected product.
        """
        if self.entered_sum >= self.selected_product['total_price']:
            print("Zahlung erfolgreich.")
            return True
        else:
            remaining = self.selected_product['total_price'] - self.entered_sum
            print(f"Nicht genug Geld. Noch zu zahlen: {remaining:.2f} €")
            return False

    def process_change(self):
        """
        Process and return change if necessary.
        """
        change = self.entered_sum - self.selected_product['total_price']
        if change > 0:
            change_banknotes = self.banknotes_manager.sumToBanknotes(change)
            formatted_change = self.banknotes_manager.formatBanknotes(change_banknotes)
            print(f"Wechselgeld: {formatted_change}")
        else:
            print("Kein Wechselgeld nötig.")
        return change

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
            self.stock_manager.remove_produkt(self.selected_product['name'], self.selected_product['quantity'])  # Bestand aktualisieren
            self.transaction_logger.Save(self.selected_product['name'])
            print(f"Produkt {self.selected_product['name']} ausgegeben.")
            self.reset_transaction()
        else:
            print("Transaktion fehlgeschlagen. Bitte mehr Geld eingeben.")

    def reset_transaction(self):
        """
        Reset the transaction by clearing the selected product and entered sum.
        """
        self.selected_product = None  # Ausgewähltes Produkt zurücksetzen
        self.entered_sum = 0  # Eingegebene Summe zurücksetzen