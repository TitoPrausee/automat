# Liste der unterstützten Banknoten
supportedBanknotes = [10, 5, 2, 1]  # Unterstützte Banknotenwerte in absteigender Reihenfolge

# Funktion zur Umrechnung einer Summe in Banknoten
def sumToBanknotes(sum):
    """
    Rechnet eine gegebene Summe in die minimale Anzahl von Banknoten um.

    :param sum: Die Geldsumme, die in Banknoten umgerechnet werden soll.
    :return: Ein Dictionary mit Banknotenwerten als Schlüssel und deren Anzahl als Werte.
    """
    banknotes = {}  # Dictionary zum Speichern der Anzahl jeder Banknote
    for note in supportedBanknotes:
        # Den Notenwert so lange von der Summe abziehen, bis die Summe kleiner als die Note ist
        while sum >= note:
            sum -= note  # Reduzieren der Summe um den Wert der Banknote
            banknotes[str(note)] = banknotes.get(str(note), 0) + 1  # Erhöhen der Anzahl der Banknote
    return banknotes  # Rückgabe des Dictionary mit den Banknoten

# Funktion zum Formatieren von Banknoten als String
def formatBanknotes(banknoteDict):
    """
    Formatiert ein Dictionary mit Banknoten in einen lesbaren String.

    :param banknoteDict: Ein Dictionary mit Banknotenwerten als Schlüssel und deren Anzahl als Werte.
    :return: Ein String, der die Anzahl jeder Banknote auflistet.
    """
    # Erstellen einer Liste mit formatierten Strings für jede Banknote (z. B. "10€ x 2")
    formatted_list = [f"{note}€ x {count}" for note, count in banknoteDict.items()]
    return ", ".join(formatted_list)  # Verbinden der formatierten Strings mit Kommas und Rückgabe des Ergebnisses