from itertools import combinations

# zbior = {'AUD': 1.5199102417, 'BGN': 1.7912203523, 'BRL': 4.9277007261,
#          'CAD': 1.3488401847, 'CHF': 0.8680701256, 'CNY': 7.195641307,
#          'CZK': 22.7345528033, 'DKK': 6.8551209922, 'EUR': 0.9193601617,
#          'GBP': 0.7869401354, 'HKD': 7.8204008729, 'HRK': 7.0198913213,
#          'HUF': 351.2355411336, 'IDR': 15601.935333516, 'ILS': 3.7596006589,
#          'INR': 83.1342544268, 'ISK': 137.1453052214, 'JPY': 148.1459827849,
#          'KRW': 1338.1732786096, 'MXN': 17.1646425795, 'MYR': 4.7162007066,
#          'NOK': 10.5237117679, 'NZD': 1.6343702936, 'PHP': 55.8325181871,
#          'PLN': 4.0292606083, 'RON': 4.5737805864, 'RUB': 89.5478337666,
#          'SEK': 10.4797216232, 'SGD': 1.3438102083, 'THB': 35.5268665026,
#          'TRY': 30.1538545449, 'USD': 1, 'ZAR': 18.9318020931}

def kombinacje(zbior):

    # Uzyskanie wszystkich kombinacji trzyelementowych kluczy
    kombinacje_kluczy = list(combinations(zbior.keys(), 3))

    # Obliczanie wyników mnożenia dla każdej kombinacji
    wyniki_mnozenia = [
        (zbior['EUR'] / zbior[klucz1]) * (zbior[klucz1] / zbior[klucz2]) * (
                    zbior[klucz2] / zbior[klucz3]) * (
                    zbior[klucz3] / zbior['EUR']) for klucz1, klucz2, klucz3 in
        kombinacje_kluczy]

    # Tworzenie słownika wyników
    slownik_wynikow = dict(zip(kombinacje_kluczy, wyniki_mnozenia))

    return slownik_wynikow


"""
    ========================================================================================
    Najważniejszy rezultat funkcji to słownik wszystkich kombinacji: "slownik_wynikow"
    
    {('TRY', 'USD', 'ZAR'): 1.00000}
    
    Drukowanie słownika wyników
    for kombinacja, wynik in (slownik_wynikow.items()):
        print(f"{kombinacja}: {wynik:.5F}")
    
"""
