# Transaction Management
# =======================
# Handles the transaction process including product selection, payment,
# stock management, transaction logging, and change processing.

from Backend.DataAccessors.Stock import Stock  # Use the Stock class from Stock.py

class TransactionManager:
    """
    Manages a transaction including product selection, payment processing,
    stock updates, and transaction logging.
    """

    def __init__(self, price_calculator, stock_manager, transaction_logger, banknotes_manager):
        """
        Initialize the TransactionManager with required managers and utilities.

        :param price_calculator: Instance of PriceCalculator to calculate product prices.
        :param stock_manager: Instance of Stock class to manage product stock.
        :param transaction_logger: Logger to record transaction details.
        :param banknotes_manager: Manager to handle banknotes and change.
        """
        self.price_calculator = price_calculator  # Handles price calculations for selected products
        self.stock_manager = stock_manager  # Manages product stock
        self.transaction_logger = transaction_logger  # Logs transaction details
        self.banknotes_manager = banknotes_manager  # Manages banknotes and change
        self.selected_product = None  # Stores details of the selected product
        self.entered_sum = 0  # Accumulated sum of money entered by the user

    def select_product(self, product_name, quantity=1):
        """
        Select a product and store its price and details after checking stock availability.

        :param product_name: The name of the product to be selected.
        :param quantity: The quantity of the product to be selected (default is 1).
        :return: True if the product is available and selected successfully, False otherwise.
        """
        if not self.stock_manager.is_in_stock(product_name, quantity):
            print(f"The product {product_name} is out of stock or the requested quantity is not available.")
            return False

        # Calculate the total price using the PriceCalculator
        total_price = self.price_calculator.get_price(product_name) * quantity
        self.selected_product = {
            'name': product_name,
            'quantity': quantity,
            'total_price': total_price
        }
        print(f"Product selected: {product_name}, Quantity: {quantity}, Price: {total_price:.2f} €")
        return True

    def enter_money(self, amount):
        """
        Enter a monetary amount and add it to the current total entered sum.

        :param amount: The monetary amount entered by the user.
        """
        if self.selected_product:
            self.entered_sum += amount
            print(f"Entered amount: {self.entered_sum:.2f} €")
        else:
            print("No product has been selected.")

    def check_payment(self):
        """
        Check if the entered amount is sufficient for the selected product.

        :return: True if the entered amount is sufficient, False otherwise.
        """
        if self.entered_sum >= self.selected_product['total_price']:
            print("Payment successful.")
            return True
        else:
            remaining = self.selected_product['total_price'] - self.entered_sum
            print(f"Not enough money. Still to pay: {remaining:.2f} €")
            return False

    def process_change(self):
        """
        Process and return change if necessary.

        :return: The amount of change to be returned.
        """
        change = self.entered_sum - self.selected_product['total_price']
        if change > 0:
            # Convert the change into banknotes and format it for display
            change_banknotes = self.banknotes_manager.sumToBanknotes(change)
            formatted_change = self.banknotes_manager.formatBanknotes(change_banknotes)
            print(f"Change: {formatted_change}")
        else:
            print("No change needed.")
        return change

    def finalize_transaction(self):
        """
        Finalize the transaction: check payment, process change, update stock,
        log the transaction, and reset the transaction.
        """
        if self.selected_product is None:
            print("No transaction can be processed. Product not available.")
            return

        if self.check_payment():
            # Process the change and update the stock
            self.process_change()
            self.stock_manager.remove_produkt(self.selected_product['name'], self.selected_product['quantity'])  # Update stock
            self.transaction_logger.Save(self.selected_product['name'])  # Log the transaction
            print(f"Product {self.selected_product['name']} dispensed.")
            self.reset_transaction()  # Reset the transaction
        else:
            print("Transaction failed. Please enter more money.")

    def reset_transaction(self):
        """
        Reset the transaction by clearing the selected product and entered sum.
        """
        self.selected_product = None  # Clear the selected product
        self.entered_sum = 0  # Reset the entered sum