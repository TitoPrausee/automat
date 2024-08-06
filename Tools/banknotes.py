supportedBanknotes = [10, 5, 2, 1]


def sumToBanknotes(sum):
    """
    This function takes a sum as input and returns a dictionary with the number of each banknote needed.
    """
    banknotes = {}
    for note in supportedBanknotes:
        while sum >= note:
            sum -= note
            banknotes[str(note)] = banknotes[str(note)] + \
                1 if str(note) in banknotes else 1
    return banknotes


def formatBanknotes(banknoteDict):
    """
    This function takes a dictionary of banknotes and returns a formatted string.
    """
    formatted_list = [f"{note}€ x {count}" for note,
                      count in banknoteDict.items()]
    return ", ".join(formatted_list)
