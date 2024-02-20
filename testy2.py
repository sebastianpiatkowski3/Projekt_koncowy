from flask import Flask, render_template
import freecurrencyapi
from file_reader import Reader  # klasa wczytująca API_key oraz symbole walut

app = Flask(__name__)
app.config["SECRET_KEY"] = "psnt"  # Klucz prywatny aplikacji dla celów m.in. bezpieczeństwa

def separator():
    print("-" * 60)

# Inicjalizacja klienta API
reader = Reader()
api_key, error_key = reader.load_key()
if error_key:
    separator()
    print(error_key)
    exit(1)

# client = freecurrencyapi.Client(api_key)
# status_klienta = client.status()
# kursy = client.latest()['data']
kursy = {'AUD': 1.5199102417, 'BGN': 1.7912203523, 'BRL': 4.9277007261, 'CAD': 1.3488401847, 'CHF': 0.8680701256, 'CNY': 7.195641307, 'CZK': 22.7345528033, 'DKK': 6.8551209922, 'EUR': 0.9193601617, 'GBP': 0.7869401354, 'HKD': 7.8204008729, 'HRK': 7.0198913213, 'HUF': 351.2355411336, 'IDR': 15601.935333516, 'ILS': 3.7596006589, 'INR': 83.1342544268, 'ISK': 137.1453052214, 'JPY': 148.1459827849, 'KRW': 1338.1732786096, 'MXN': 17.1646425795, 'MYR': 4.7162007066, 'NOK': 10.5237117679, 'NZD': 1.6343702936, 'PHP': 55.8325181871, 'PLN': 4.0292606083, 'RON': 4.5737805864, 'RUB': 89.5478337666, 'SEK': 10.4797216232, 'SGD': 1.3438102083, 'THB': 35.5268665026, 'TRY': 30.1538545449, 'USD': 1, 'ZAR': 18.9318020931}


def przelicz_waluty(waluta_poczatkowa, waluta_docelowa, kursy):
    if waluta_poczatkowa not in kursy or waluta_docelowa not in kursy:
        return "Brak informacji o kursie dla podanych walut."
    kurs_poczatkowy = kursy[waluta_poczatkowa]
    kurs_docelowy = kursy[waluta_docelowa]
    kwota_w_docelowej = kurs_docelowy / kurs_poczatkowy
    return kwota_w_docelowej

waluta = []
# Przykładowe użycie
for key, value in kursy.items():
    waluta.append(key)

waluta_poczatkowa = 'USD'  # Przykładowa waluta początkowa
for i in range(0, len(waluta)):
    waluta_docelowa =   waluta[i]  # Przykładowa waluta docelowa
    wynik = przelicz_waluty(waluta_poczatkowa, waluta_docelowa, kursy)
    print(f"{waluta_poczatkowa} to {wynik:.2f} {waluta_docelowa}")

import itertools


def przelicz(waluta1, waluta2, waluta3, kursy):
    if waluta1 not in kursy or waluta2 not in kursy or waluta3 not in kursy:
        return "Brak informacji o kursie dla podanych walut."

    kurs1 = kursy[waluta1]
    kurs2 = kursy[waluta2]
    kurs3 = kursy[waluta3]

    return kurs1, kurs2, kurs3


# Tworzenie kombinacji walut
waluty = ['AUD', 'BGN', 'BRL']
kombinacje_walut = list(itertools.product(waluty, repeat=3))

# Przeliczanie dla każdej kombinacji
for kombinacja in kombinacje_walut:
    wynik_kursow = przelicz(*kombinacja, kursy)
    print(f"Kursy dla {kombinacja}: {wynik_kursow}")

import itertools


def przelicz(waluta1, waluta2, waluta3, kursy):
    if waluta1 not in kursy or waluta2 not in kursy or waluta3 not in kursy:
        return "Brak informacji o kursie dla podanych walut."

    kurs1 = kursy[waluta1]
    kurs2 = kursy[waluta2]
    kurs3 = kursy[waluta3]

    iloczyn_kursow = kurs1 * kurs2 * kurs3

    return iloczyn_kursow


# Tworzenie kombinacji walut
waluty = ['AUD', 'BGN', 'BRL']
kombinacje_walut = list(itertools.product(waluty, repeat=3))

# Policzenie iloczynu dla każdej kombinacji
for kombinacja in kombinacje_walut:
    wynik_iloczynu = przelicz(*kombinacja, kursy)
    print(f"Iloczyn kursów dla {kombinacja}: {wynik_iloczynu}")


@app.route('/')
def index():
    """
    Główna strona aplikacji. Wyświetla najnowsze kursy walut.
    """

    return render_template('index.html', kursy=kursy)

@app.route('/kombinacje')
def kombinacje():

    return render_template('kombinacje.html')

@app.route('/status')
def status():
    """
    Strona statusu. Wyświetla status klienta API.
    """
    client_status_dict = {
        'account_id' : 'id',
        'quotas' : '',
    }
    return render_template('charts.html', status=client_status_dict)

@app.route('/about')
def about():
    """
    Strona o nas. Wyświetla informacje o aplikacji.
    """
    return render_template('about.html')

# if __name__ == "__main__":
#     app.run(debug=True)
