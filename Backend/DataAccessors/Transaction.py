import csv  # Module for working with CSV files
import os   # Module for working with operating system functionalities

# 1. Class to manage transaction data
class Transaction:
    """
    Handles the saving of transaction data to a CSV file.

    Attributes:
        dirname: Directory path to the location of the CSV file.
        csvPath: Full path to the transactions CSV file.
    """

    # 1.1 Static attributes for paths
    dirname = os.path.dirname(os.path.dirname(__file__))  # Directory name for the CSV directory
    csvPath = os.path.join(dirname, 'CSV/transactions.csv')  # Full path to the CSV file

    # 1.2 Method to save a transaction
    @staticmethod
    def Save(item):
        """
        Save the transaction data to the CSV file.

        :param item: The item to be saved in the transaction log.
        """
        # Open the CSV file in append mode ('a') to add new transactions
        with open(Transaction.csvPath, 'a', newline='') as csvFile:
            # Create a DictWriter to write a row with the 'item' column
            writer = csv.DictWriter(csvFile, ['item'])  # CSV writer with 'item' as the column name
            # Write the item to the CSV file
            writer.writerow({'item': item})  # Write the passed item into the CSV file