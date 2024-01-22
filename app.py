from flask import Flask, render_template, request, flash, redirect
from url import get_exchange
from kombinacje import kombinacje

app = Flask(__name__)

app.config["SECRET_KEY"] = "psnt"  # Klucz prywatny aplikacji dla celów m.in. bezpieczeństwa

# Pobranie danych z API url = "https://api.nbp.pl/api/exchangerates/tables/A"
tablea_list, tablea_dict = get_exchange()

ilosc_walut = len(tablea_list) - 6

# Pobranie wszystkich kombinacji trójek walut: np. ('AUD', 'BGN', 'BRL') i ich iloczynów
iloczyny_dict = kombinacje(tablea_dict)

above_one = 0
equal_to_one = 0
less_than_one = 0
posortowany_słownik = dict(sorted(iloczyny_dict.items(), key=lambda x: x[1], reverse=True))
for wartosc in posortowany_słownik.values():
    if wartosc > 1:
       above_one += 1
    elif wartosc == 1:
        equal_to_one += 1
    elif wartosc < 1:
        less_than_one += 1

above_one = f"{above_one},         {above_one*100/len(posortowany_słownik):.1F} %"
equal_to_one = f"{equal_to_one},         {equal_to_one*100/len(posortowany_słownik):.1F} %"
less_than_one = f"{less_than_one},         {less_than_one*100/len(posortowany_słownik):.1F} %"

slownik_strona = {}
# Dodaj pierwsze 10 elementów do nowego słownika
for klucz, wartosc in posortowany_słownik.items():
    slownik_strona[klucz] = wartosc
    if len(slownik_strona) == 10:
        break


pierwsze_10_wieksze_1 = {}
# Iteruj po kluczach i wartościach i dodaj do listy pierwsze 10 wartości równych 1
for klucz, wartosc in iloczyny_dict.items():
    if wartosc > 1 and len(pierwsze_10_wieksze_1) < 10:
        pierwsze_10_wieksze_1[klucz]=wartosc

pierwsze_10_rowne_1 = {}
# Iteruj po kluczach i wartościach i dodaj do listy pierwsze 10 wartości równych 1
for klucz, wartosc in iloczyny_dict.items():
    if wartosc == 1 and len(pierwsze_10_rowne_1) < 10:
        pierwsze_10_rowne_1[klucz]=wartosc

pierwsze_10_mniejsze_1 = {}
# Iteruj po kluczach i wartościach i dodaj do listy pierwsze 10 wartości równych 1
for klucz, wartosc in iloczyny_dict.items():
    if wartosc < 1 and len(pierwsze_10_mniejsze_1) < 10:
        pierwsze_10_mniejsze_1[klucz]=wartosc

@app.route('/')
def index():
    return render_template('index.html', dane=tablea_list)

@app.route('/kombinacje')
def kombinacje():
    return render_template('kombinacje.html', dane = slownik_strona,
                           ilosc_walut=ilosc_walut,
                           pierwsze_10_wieksze_1=pierwsze_10_wieksze_1,
                           pierwsze_10_rowne_1=pierwsze_10_rowne_1,
                           pierwsze_10_mniejsze_1=pierwsze_10_mniejsze_1,
                           above_one = above_one,
                           equal_to_one = equal_to_one ,
                           less_than_one = less_than_one)

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/about')
def about():
    return render_template('about.html')
