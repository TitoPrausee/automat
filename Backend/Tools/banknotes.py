# 1. Liste der unterstützten Banknoten
supportedBanknotes = [10, 5, 2, 1]  # Unterstützte Banknoten in absteigender Reihenfolge

# 2. Funktion zur Umrechnung einer Summe in Banknoten
def sumToBanknotes(sum):
    """
    Converts a given sum into the minimum number of banknotes.

    :param sum: The sum of money to be converted into banknotes.
    :return: A dictionary with banknote denominations as keys and their counts as values.
    """
    banknotes = {}
    for note in supportedBanknotes:
        while sum >= note:
            sum -= note  # Reduziert die Summe um den Wert der Banknote
            banknotes[str(note)] = banknotes.get(str(note), 0) + 1  # Erhöht die Anzahl der Banknoten
    return banknotes

# 3. Funktion zur Formatierung der Banknoten als String
def formatBanknotes(banknoteDict):
    """
    Formats a dictionary of banknotes into a readable string.

    :param banknoteDict: A dictionary with banknote denominations as keys and their counts as values.
    :return: A string that lists the number of each banknote.
    """
    formatted_list = [f"{note}€ x {count}" for note, count in banknoteDict.items()]  # Formatierung der Banknoten
    return ", ".join(formatted_list)  # Rückgabe des formatierten Strings
