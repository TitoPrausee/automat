# TransactionManager Class Definition
# ------------------------------------
# Manages a transaction process, including product selection, payment entry,
# payment verification, change processing, and transaction finalization.

class TransactionManager:
    def __init__(self, price_calculator, banknotes_manager):
        """
        Initialize the TransactionManager with a price calculator and banknotes manager.
        
        :param price_calculator: Function to calculate the total price of selected products.
        :param banknotes_manager: Object to manage banknote-related operations.
        """
        self.price_calculator = price_calculator  # Function for price calculation
        self.banknotes_manager = banknotes_manager  # Manager for handling banknotes
        self.selected_product = None  # Holds the selected product details
        self.entered_sum = 0  # Accumulated entered amount by the user

    def select_product(self, product_name, quantity=1):
        """
        Select a product and store its price and details.

        :param product_name: Name of the product selected.
        :param quantity: Number of units of the product selected.
        """
        total_price = self.price_calculator(product_name, quantity)
        self.selected_product = {
            'name': product_name,
            'quantity': quantity,
            'total_price': total_price
        }
        print(f"Produkt gewählt: {product_name}, Menge: {quantity}, Preis: {total_price:.2f} €")

    def enter_money(self, amount):
        """
        Enter a monetary amount and add it to the current total entered sum.

        :param amount: The amount of money being entered by the user.
        """
        self.entered_sum += amount
        print(f"Eingegebener Betrag: {self.entered_sum:.2f} €")

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

    def process_change(self):
        """
        Process and return change if necessary.

        :return: The amount of change to be returned.
        """
        change = self.entered_sum - self.selected_product['total_price']
        if change > 0:
            # Convert the change amount to banknotes
            change_banknotes = self.banknotes_manager.sumToBanknotes(change)
            # Format the banknotes for display
            formatted_change = self.banknotes_manager.formatBanknotes(change_banknotes)
            print(f"Wechselgeld: {formatted_change}")
        else:
            print("Kein Wechselgeld nötig.")
        return change

    def finalize_transaction(self):
        """
        Finalize the transaction: check payment, process change, and reset the transaction.

        This method handles the overall flow of the transaction once money is entered.
        """
        if self.check_payment():
            self.process_change()
            print(f"Produkt {self.selected_product['name']} ausgegeben.")
            self.reset_transaction()
        else:
            print("Transaktion fehlgeschlagen. Bitte mehr Geld eingeben.")

    def reset_transaction(self):
        """
        Reset the transaction by clearing the selected product and entered sum.
        """
        self.selected_product = None
        self.entered_sum = 0


# Example Usage
# --------------
# This demonstrates how to use the TransactionManager class.
if __name__ == '__main__':
    # Import necessary modules from the Backend.Tools package
    from Tools.price_calculator import calculate_total_price
    from Tools.banknotes import sumToBanknotes, formatBanknotes

    # Instantiate the price calculator and banknotes manager
    price_calculator = calculate_total_price
    banknotes_manager = type('BanknotesManager', (), {'sumToBanknotes': sumToBanknotes, 'formatBanknotes': formatBanknotes})()

    # Create a TransactionManager instance
    transaction_manager = TransactionManager(price_calculator, banknotes_manager)

    # Simulate a transaction
    transaction_manager.select_product('cola', 2)
    transaction_manager.enter_money(5)
    transaction_manager.finalize_transaction()
