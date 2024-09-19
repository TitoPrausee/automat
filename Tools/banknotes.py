# 1. List of supported banknotes
supportedBanknotes = [10, 5, 2, 1]  # Supported banknote denominations in descending order

# 2. Function to convert a sum into banknotes
def sumToBanknotes(sum):
    """
    Converts a given sum into the minimum number of banknotes.

    :param sum: The sum of money to be converted into banknotes.
    :return: A dictionary with banknote denominations as keys and their counts as values.
    """
    banknotes = {}  # Dictionary to store the count of each banknote
    for note in supportedBanknotes:
        # Keep subtracting the note value from the sum until the sum is smaller than the note
        while sum >= note:
            sum -= note  # Reduce the sum by the value of the banknote
            banknotes[str(note)] = banknotes.get(str(note), 0) + 1  # Increment the count of the banknote
    return banknotes  # Return the dictionary of banknotes

# 3. Function to format banknotes as a string
def formatBanknotes(banknoteDict):
    """
    Formats a dictionary of banknotes into a readable string.

    :param banknoteDict: A dictionary with banknote denominations as keys and their counts as values.
    :return: A string that lists the number of each banknote.
    """
    # Create a list of formatted strings for each banknote (e.g., "10€ x 2")
    formatted_list = [f"{note}€ x {count}" for note, count in banknoteDict.items()]
    return ", ".join(formatted_list)  # Join the formatted strings with commas and return the result