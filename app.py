

from flask import Flask, render_template, request, flash, redirect
import freecurrencyapi
klucz = "C:/users/sebas/klucz.txt"  # Plik z kluczem API
client_status_dict= {}

app = Flask(__name__)

app.config["SECRET_KEY"] = "psnt"  # Klucz prywatny aplikacji dla celów m.in. bezpieczeństwa


with open(klucz) as zawartosc_pliku:
    apikey = zawartosc_pliku.read().strip()  # Usunięcie ewentualnych białych znaków na początku i końcu
if apikey:
    client = freecurrencyapi.Client(apikey)
else:
    wczytywanie = False
    flash(f"Błąd: Plik \"{klucz}\" jest pusty lub nie zawiera prawidłowego klucza.")



@app.route('/')
def index():
    kursy = {'AUD': 1.5263402006, 'BGN': 1.7914602142, 'BRL': 4.9349407964, 'CAD': 1.3499002044, 'CHF': 0.8642801516, 'CNY': 7.1952110979, 'CZK': 22.7080727839, 'DKK': 6.8496408238, 'EUR': 0.918460133, 'GBP': 0.7888101481, 'HKD': 7.81916121, 'HRK': 7.0190712163, 'HUF': 348.7454373584, 'IDR': 15615.630404131, 'ILS': 3.7924906612, 'INR': 83.1541531204, 'ISK': 137.5734757264, 'JPY': 148.1056956932, 'KRW': 1342.6442011241, 'MXN': 17.1948332549, 'MYR': 4.7150405437, 'NOK': 10.4991614381, 'NZD': 1.6357301993, 'PHP': 55.8925090032, 'PLN': 4.0391104838, 'RON': 4.5695405654, 'RUB': 88.9826805086, 'SEK': 10.4385014086, 'SGD': 1.3440801752, 'THB': 35.5868466639, 'TRY': 30.1273151842, 'USD': 1, 'ZAR': 19.0595827862}
    return render_template('index.html', kursy=kursy)


@app.route('/status')
def status():
    status_klienta = client.status()
    print(status_klienta)
    account_id =  status_klienta['account_id']
    quotas = list(status_klienta.keys())[1]
    client_status_dict = {
        'account_id' : account_id,
        quotas : '',
        'month total: ' :  status_klienta['quotas']['month']['total'],
        'month used: ' : status_klienta['quotas']['month']['used'],
        'month remaining: ' : status_klienta['quotas']['month']['remaining'],
    }
    return render_template('status.html', status=client_status_dict)

@app.route('/about')
def about():
    return render_template('about.html')

def separator():
    print("-" * 60)


# separator()
#
# kursy = client.latest()
# print(kursy)
# separator()
#
# result = client.historical('2022-02-02')
# print(result)
# separator()
#
# result = client.currencies(currencies=['EUR', 'CAD'])
# print(result)
# separator()
#
# for value in kursy.values():
#     print(value)
#
# separator()
# eur_rate = kursy['data']['EUR']
# print(eur_rate)
