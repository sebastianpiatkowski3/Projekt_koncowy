from flask import Flask, render_template, request, flash, redirect
from url import get_exchange
from kombinacje import kombinacje
from plotly import utils
import plotly.express as px
import pandas as pd
import json
from plotly import graph_objs as go
import matplotlib.pyplot as plt
import mpld3
import seaborn as sns


app = Flask(__name__)

app.config["SECRET_KEY"] = "psnt"  # Klucz prywatny aplikacji dla celów m.in. bezpieczeństwa
file = 'GER40_2024.csv'  # Plik CSV z danymi
# Pobranie danych z API url = "https://api.nbp.pl/api/exchangerates/tables/A"
tablea_list, tablea_dict = get_exchange()

ilosc_walut = len(tablea_list) - 6

def read_data(file):
    # Lista z nazwami kolumn
    nazwy_kolumn = ['d', 'g', 'o', 'h', 'l', 'c', 'w']
    # Wczytaj dane z pliku CSV
    df = pd.read_csv(file , sep = ',' , header = None, names=nazwy_kolumn)
    df['datetime'] = pd.to_datetime(df['d'] + ' ' + df['g'])
    return df




df = read_data(file)
time_difference = df.iloc[-1]['datetime'] - df.iloc[0]['datetime']

# # Pobranie wszystkich kombinacji trójek walut: np. ('AUD', 'BGN', 'BRL') i ich iloczynów
# iloczyny_dict = kombinacje(tablea_dict)
#
# above_one = 0
# equal_to_one = 0
# less_than_one = 0
# posortowany_słownik = dict(sorted(iloczyny_dict.items(), key=lambda x: x[1], reverse=True))
# for wartosc in posortowany_słownik.values():
#     if wartosc > 1:
#        above_one += 1
#     elif wartosc == 1:
#         equal_to_one += 1
#     elif wartosc < 1:
#         less_than_one += 1
#
# above_one = f"{above_one},         {above_one*100/len(posortowany_słownik):.1F} %"
# equal_to_one = f"{equal_to_one},         {equal_to_one*100/len(posortowany_słownik):.1F} %"
# less_than_one = f"{less_than_one},         {less_than_one*100/len(posortowany_słownik):.1F} %"
#
# slownik_strona = {}
# # Dodaj pierwsze 10 elementów do nowego słownika
# for klucz, wartosc in posortowany_słownik.items():
#     slownik_strona[klucz] = wartosc
#     if len(slownik_strona) == 10:
#         break
#
#
# pierwsze_10_wieksze_1 = {}
# # Iteruj po kluczach i wartościach i dodaj do listy pierwsze 10 wartości równych 1
# for klucz, wartosc in iloczyny_dict.items():
#     if wartosc > 1 and len(pierwsze_10_wieksze_1) < 10:
#         pierwsze_10_wieksze_1[klucz]=wartosc
#
# pierwsze_10_rowne_1 = {}
# # Iteruj po kluczach i wartościach i dodaj do listy pierwsze 10 wartości równych 1
# for klucz, wartosc in iloczyny_dict.items():
#     if wartosc == 1 and len(pierwsze_10_rowne_1) < 10:
#         pierwsze_10_rowne_1[klucz]=wartosc
#
# pierwsze_10_mniejsze_1 = {}
# # Iteruj po kluczach i wartościach i dodaj do listy pierwsze 10 wartości równych 1
# for klucz, wartosc in iloczyny_dict.items():
#     if wartosc < 1 and len(pierwsze_10_mniejsze_1) < 10:
#         pierwsze_10_mniejsze_1[klucz]=wartosc

periods_1 = [5, 10 , 20 , 30, 45 , 70 , 100]
periods_2 = [20, 30, 50 , 100, 150, 200, 250, 300]

def count_crossings(df):
    results = []
    time_difference = df.iloc[-1]['datetime'] - df.iloc[0]['datetime']
    if time_difference == 0:
        time_difference = 1
    ind = 0
    pips_per_day_df = pd.DataFrame(columns = ['sma1' , 'sma2' , 'ppd' , 'p_t' , 's_c'])


    for period1 in periods_1:
        for period2 in periods_2:
            if period1 < period2:
                print(f'=======================period1: {period1} , period2: {period2}')
                # Oblicz średnią ruchomą:
                sma1 = df['c'].rolling(window = period1).mean()
                df['sma1'] = sma1
                sma2 = df['c'].rolling(window = period2).mean()
                df['sma2'] = sma2

                # Znajdź momenty przecięcia (kiedy sma1 przecina sma2)
                crossings_upward = (sma1.shift(1) > sma2.shift(1)) & (sma1 < sma2)  # cena spada:  sprzedaj
                crossings_downward = (sma1.shift(1) < sma2.shift(1)) & (sma1 > sma2)  # cena rosnie: kupuj
                # Dodaj kolumnę 'crossings_upward' do ramki danych
                df['crossings_upward'] = crossings_upward
                df['crossings_downward'] = crossings_downward

                df['crossings'] = df['crossings_upward'] | df['crossings_downward']
                df['crossings'].fillna(False , inplace = True)
                print(f'df 116: \n{df[1:15]}')

                momenty = df[df['crossings']]
                print(f'momenty 118: \n{momenty}')
                momenty_print = momenty[['c' , 'crossings_upward' , 'crossings_downward' , 'crossings']]


                # Oblicz różnicę dla kolumny 'c'
                momenty['c_diff'] = momenty['c'].diff()  # tu  liczę różnice, czyli profit
                momenty['c_diff'] = momenty['c_diff'].fillna(0)
                print(f' momenty 124: \n{momenty[0:15]}')
                # Zastosuj warunki i pomnóż przez -1
                condition = (momenty['crossings_upward'].shift(-1) == True) & (momenty['c'].shift(-1) < momenty['c'])
                momenty.loc[condition , 'c_diff'] *= -1
                momenty['c_diff'] = momenty['c_diff'] - 1
                # print only 'c' 'c_diff' 'crossings_upward' 'crossings_downward' 'crossings' from momenty
                momenty_print = momenty[['c' , 'c_diff' , 'crossings_upward' , 'crossings_downward' , 'crossings']]
                print(f' momenty_print 130: \n{momenty_print[0:15]}')

                diffs = momenty['c_diff']
                print(f'diffs 133: \n{diffs[0:15]}')

                # sum all absolute values of data from the second column of diffs
                profit_total = round(diffs.sum(), 0)
                print(f'- Profit total: {profit_total:.1f}')
                if time_difference.days < 1:
                   ppd = 1
                ppd = round(profit_total / time_difference.days , 1)
                sum_crossings = len(diffs)
                results.append({'sma1': period1 , 'sma2': period2 , 'ppd': ppd , 'p_t': profit_total , 's_c': sum_crossings})
                pips_per_day_df.loc[ind] = [period1 ,
                                            period2 , ppd ,
                                            profit_total ,
                                            sum_crossings]
                ind += 1

                print(f'- Pips per day: {ppd}')
                print(f'- ilosć crossów: {len(diffs)}')
                print(f'- Time_difference: {time_difference}')
                print(pips_per_day_df)
                print('-' * 50)
    return results


results = count_crossings(df)
print(f'=== Total profits: {results}')
results_df = pd.DataFrame(results)



@app.route('/')
def index():
    return render_template('index.html', dane=tablea_list)

@app.route('/kombinacje')
def kombinacje():
    return render_template('kombinacje.html')

@app.route('/status')
def status():
    # Rysowanie mapy ciepła
    # Przekształć 'sma1' i 'sma2' na łańcuchy znaków
    results_df['sma1'] = results_df['sma1'].astype(str)
    results_df['sma2'] = results_df['sma2'].astype(str)

    # Przekształć 'sma1' i 'sma2' na typ kategorialny z odpowiednią kolejnością
    # Tworzenie listy unikalnych wartości z kolumny 'sma1'
    unique_values_sma1 =  results_df['sma1'].unique()  # czyli:   sma1_order = ['20' , '30' , '50' , '100']  # Ustal odpowiednią kolejność
    unique_values_sma2 =  results_df['sma2'].unique()
    results_df['sma1'] = pd.Categorical(results_df['sma1'] , categories = unique_values_sma1 , ordered = True)
    results_df['sma2'] = pd.Categorical(results_df['sma2'] , categories = unique_values_sma2 , ordered = True)
    """    W Plotly Express, funkcja imshow() domyślnie tworzy komórki o równej wielkości. Jeśli zauważasz, że komórki mają różne rozmiary, może to wynikać z tego, że wartości ‘sma1’ i ‘sma2’ są używane jako numeryczne indeksy, a nie jako kategorie.
Jednakże, jeśli twoje dane ‘sma1’ i ‘sma2’ są rzeczywiście numeryczne i chcesz je przedstawić jako kategorie, możesz spróbować przekształcić te wartości na łańcuchy znaków.
W powyższym kodzie, results_df['sma1'].astype(str) i results_df['sma2'].astype(str) przekształcają ‘sma1’ i ‘sma2’ na łańcuchy znaków. Dzięki temu, każda unikalna wartość ‘sma1’ i ‘sma2’ jest traktowana jako osobna kategoria, a nie jako liczba, co powinno sprawić, że wszystkie komórki na mapie ciepła będą miały tę samą wielkość."""

    """    Przekształca DataFrame results_df tak,
    że kolumny i indeksy są określone przez wartości ‘sma1’ i ‘sma2’,
    a wartości wewnątrz są określone przez ‘p_t’.
    Następnie, używając funkcji imshow() z Plotly Express, tworzymy mapę ciepła z tych danych."""


    fig = px.imshow(results_df.pivot(index = 'sma1' , columns = 'sma2' , values = 'p_t') ,  # Dane
                    labels = dict(x = "Okresy sredniej szybkiej" , y = "Okresy sredniej wolnej" , color = "Profit") ,
                    text_auto = True, # Automatyczne wyświetlanie wartości,
                    width = 600, height = 600,  # Szerokość i wysokość wykresu
                    color_continuous_scale='blues')  # Wybierz inną paletę kolorów, jeśli chcesz

    fig.update_layout(title = 'Mapa ciepła dla danych')

    # Konwersja wykresu do HTML
    plot_html = fig.to_html(full_html = False)

    # Konwersja dataframe do HTML
    table = results_df.to_html(classes = 'table table-bordered')

    return render_template('status.html', heatmap=plot_html, mpld3=mpld3, table = table)#, plot_div=plot_div, pub_lines_JSON = all_pub_json)


@app.route('/about')
def about():
    return render_template('about.html')
