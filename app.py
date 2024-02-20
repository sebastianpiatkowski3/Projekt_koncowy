import os
from flask import Flask, render_template, request, flash, redirect, g, session
from flask_session import Session
from werkzeug.utils import secure_filename
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
import yfinance as yf
from pandas.errors import ParserError
from sqlalchemy import func , ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

app = Flask(__name__)

app.config["SECRET_KEY"] = "psnt"  # Klucz prywatny aplikacji dla celów m.in. bezpieczeństwa
app.config['SESSION_TYPE'] = 'filesystem'
app_info = {
    'db_file' : r'C:\Users\sebas\PycharmProjects\Currency\profits.db'
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profits.db'
db = SQLAlchemy(app)
Session(app)

# Inicjalizacja rozszerzenia pamięci podręcznej
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# file = 'GER40_2024.csv'  # Plik CSV z danymi
file = 'GER402.csv'  # Plik CSV z danymi
data = None

ticker_symbols = {
    "NASDAQ 100": "^NDX",
    "DAX": "^GDAXI",
    "EUR-USD": "EURUSD=X",
    "EUR-GBP": "EURGBP=X",
    "USD-GBP": "GBPUSD=X",
    "USD-JPY": "USDJPY=X",
    "USD-BTC": "BTC-USD",
    "USD-ETH": "ETH-USD"
}

timeframes = {
    "1 minute": "1m",
    "2 minutes": "2m",
    "5 minutes": "5m",
    "15 minutes": "15m",
    "30 minutes": "30m",
    "60 minutes": "60m",
    "90 minutes": "90m",
    "1 hour": "1h",
    "1 day": "1d",
    "5 days": "5d",
    "1 week": "1wk",
    "1 month": "1mo",
    "3 months": "3mo"
}

class Profits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String)
    instrument = db.Column(db.String)
    sma_slow = db.Column(db.Integer)
    sma_fast = db.Column(db.Integer)
    daily_profit = db.Column(db.Float)
    total_profit = db.Column(db.Float)
    crossover_sum = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    date_time = db.Column(db.DateTime, server_default=func.now())

with app.app_context():
    db.create_all()
    db.session.commit()

def save_data(file, instrument, sma_slow, sma_fast, daily_profit, total_profit, crossover_sum, start_date, end_date):
    try:
        new_profit = Profits(file=file, instrument=instrument, sma_slow=sma_slow, sma_fast=sma_fast, daily_profit=daily_profit, total_profit=total_profit, crossover_sum=crossover_sum, start_date=start_date, end_date=end_date)
        db.session.add(new_profit)
        db.session.commit()
        return new_profit.id
    except Exception as e:
        print(f"Błąd: {e}")
        return None

def read_data(file):
    try:
        # Lista z nazwami kolumn
        nazwy_kolumn = ['d', 'g', 'o', 'h', 'l', 'c', 'w']
        # Wczytaj dane z pliku CSV
        df = pd.read_csv(file , sep = ',' , header = None, names=nazwy_kolumn)
        df['datetime'] = pd.to_datetime(df['d'] + ' ' + df['g']) # Połącz kolumny 'd' i 'g' w jedną kolumnę 'datetime'
        return df
    except ParserError as e:
       g.flash_message = f"Błąd konwersji danych: {e}. Sprawdź format danych i spróbuj ponownie."
       return None

df = read_data(file)


def get_instrument_name(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        instrument_name = info.get('longName', symbol)  # Domyślnie ustawia "Nazwa nieznana", jeśli nie ma dostępnej nazwy
        return instrument_name
    except Exception as e:
        print(f"Błąd: {e}")
        return None

def calculate_sma(df, period):
    return df['c'].rolling(window=period).mean()

def find_crossings(df, sma1, sma2):
    crossings_upward = (sma1.shift(1) > sma2.shift(1)) & (sma1 < sma2)
    crossings_downward = (sma1.shift(1) < sma2.shift(1)) & (sma1 > sma2)
    return crossings_upward, crossings_downward

def apply_conditions(momenty):
    condition = (momenty['crossings_upward'].shift(-1) == True) & (momenty['c'].shift(-1) < momenty['c'])
    momenty.loc[condition, 'c_diff'] *= -1
    momenty.loc[:, 'c_diff'] = momenty['c_diff'] - 1

def calculate_profits(diffs, time_difference):
    total_profit = round(diffs.sum(), 0)
    interval = max(time_difference.days, 1)
    daily_profit = round(total_profit / interval, 1)
    return total_profit, daily_profit

periods_1 = [5, 10 , 20 , 30, 45 , 70 , 100]
periods_2 = [20, 30, 50 , 100, 150, 200, 250, 300]

def count_crossings(df):
    results = []
    profit_max = float('-inf')
    profit_min = float('inf')
    daily_profit_max = float('-inf')
    daily_profit_min = float('inf')
    sma1_max = float('-inf')
    sma2_max = float('-inf')
    sma1_min = float('inf')
    sma2_min = float('inf')

    time_difference = df.iloc[-1]['datetime'] - df.iloc[0]['datetime']
    if time_difference == 0:
        time_difference = 1

    for period1 in periods_1:
        for period2 in periods_2:
            if period1 < period2:
                sma1 = calculate_sma(df, period1)
                df['sma1'] = sma1
                sma2 = calculate_sma(df, period2)
                df['sma2'] = sma2

                crossings_upward, crossings_downward = find_crossings(df, sma1, sma2)

                df['crossings_upward'] = crossings_upward
                df['crossings_downward'] = crossings_downward

                df['crossings'] = df['crossings_upward'] | df['crossings_downward']
                df.fillna({'crossings': False}, inplace=True)

                momenty = df[df['crossings']]

                momenty.loc[:, 'c_diff'] = momenty['c'].diff()
                momenty.loc[:, 'c_diff'] = momenty['c_diff'].fillna(0)

                apply_conditions(momenty)

                diffs = momenty['c_diff']

                total_profit, daily_profit = calculate_profits(diffs, time_difference)

                interval = time_difference.days
                if interval < 1:
                    interval = 1

                crossover_sum = len(diffs)
                results.append({'sma_slow': period1, 'sma_fast': period2, 'daily_profit': daily_profit,
                                'total_profit': total_profit, 'crossover_sum': crossover_sum})

                # Zapisz wyniki do bazy danych
                # save_data(session['filename'], 'GER40', period1, period2, daily_profit, total_profit, crossover_sum, df.iloc[0]['datetime'], df.iloc[-1]['datetime'])

                if total_profit > profit_max:
                    profit_max = total_profit
                    daily_profit_max = daily_profit
                    sma1_max = period1
                    sma2_max = period2
                    df_max = df.copy()
                if total_profit < profit_min:
                    profit_min = total_profit
                    daily_profit_min = daily_profit
                    sma1_min = period1
                    sma2_min = period2
                    df_min = df.copy()
    return (results,
            profit_max, profit_min, daily_profit_max, daily_profit_min, sma1_max, sma2_max, sma1_min, sma2_min, df_max, df_min)


data = None
opis = ''

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.form:
        # Sprawdź, który przycisk został naciśnięty
        if 'submit_data' in request.form:
            # Pobierz dane z formularza
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            instrument = request.form.get('ticker')
            timeframe = request.form.get('timeframe')
            # Pobierz dane z yfinance
            data = yf.download(instrument , start = start_date , end = end_date , interval = timeframe)
            session['data'] = data  # Zapisz dane w sesji
            nazwa_instrumentu = get_instrument_name(instrument)
            session['opis'] = f'Dane dla {nazwa_instrumentu} w okresie od {start_date} do {end_date} z interwałem {timeframe}.'
        elif 'submit_file' in request.form:
            csv_file = request.files['csv']
            session['filename'] = csv_file.filename
            filename = session.get('filename' , '')
            data = read_data(csv_file)
            session['data'] = data  # Zapisz dane w sesji
            outcome = count_crossings(data)
            session['results_df'] = pd.DataFrame(outcome[0])
            session['outcome'] = outcome
            session['opis'] = f'Dane z pliku: {filename}'
    # Sprawdź, czy 'opis' istnieje w sesji przed użyciem
    session['opis'] = session.get('opis', '')
    # Sprawdź, czy data jest różne od None, zanim użyjesz to_html
    data_html = session['data'].to_html(classes = 'table table-bordered') if session['data'] is not None else ''
    return render_template('index.html',
                           data_html=data_html,
                           data = session['data'],
                           outcome = session['outcome'],
                           results_df = session['results_df'],
                           opis = session['opis'],
                           filename = session.get('filename', ''))


@app.route('/charts')
@cache.cached(timeout=60)  # Cache na 60 sekund
def charts():
    outcome = session['outcome']
    df_max = outcome[9]
    df_min = outcome[10]
    profit_max = outcome[1]
    profit_min = outcome[2]
    daily_profit_max = outcome[3]
    daily_profit_min = outcome[4]
    sm1_max = outcome[5]
    sm2_max = outcome[6]
    sm1_min = outcome[7]
    sm2_min = outcome[8]

    plot_color = '#1F1F1F'
    font_color = '#D3D3D3'
    # Rysowanie mapy ciepła
    # Przekształć 'sma1' i 'sma2' na łańcuchy znaków
    results_df = session['results_df']
    results_df['sma_slow'] = results_df['sma_slow'].astype(str)
    results_df['sma_fast'] = results_df['sma_fast'].astype(str)
    # Przekształć 'sma1' i 'sma2' na typ kategorialny z odpowiednią kolejnością
    # Tworzenie listy unikalnych wartości z kolumny 'sma1'
    unique_values_sma1 =  results_df['sma_slow'].unique()  # czyli:   sma1_order = ['20' , '30' , '50' , '100']  # Ustal odpowiednią kolejność
    unique_values_sma2 =  results_df['sma_fast'].unique()
    results_df['sma_slow'] = pd.Categorical(results_df['sma_slow'] , categories = unique_values_sma1 , ordered = True)
    results_df['sma_fast'] = pd.Categorical(results_df['sma_fast'] , categories = unique_values_sma2 , ordered = True)
    """    W Plotly Express, funkcja imshow() domyślnie tworzy komórki o równej wielkości. Jeśli zauważasz, że komórki mają różne rozmiary, może to wynikać z tego, że wartości ‘sma1’ i ‘sma2’ są używane jako numeryczne indeksy, a nie jako kategorie.
Jednakże, jeśli twoje dane ‘sma1’ i ‘sma2’ są rzeczywiście numeryczne i chcesz je przedstawić jako kategorie, możesz spróbować przekształcić te wartości na łańcuchy znaków.
W powyższym kodzie, results_df['sma1'].astype(str) i results_df['sma2'].astype(str) przekształcają ‘sma1’ i ‘sma2’ na łańcuchy znaków. Dzięki temu, każda unikalna wartość ‘sma1’ i ‘sma2’ jest traktowana jako osobna kategoria, a nie jako liczba, co powinno sprawić, że wszystkie komórki na mapie ciepła będą miały tę samą wielkość."""
    """    Przekształca DataFrame results_df tak,
    że kolumny i indeksy są określone przez wartości ‘sma1’ i ‘sma2’,
    a wartości wewnątrz są określone przez ‘p_t’.
    Następnie, używając funkcji imshow() z Plotly Express, tworzymy mapę ciepła z tych danych."""

    fig = px.imshow(results_df.pivot(index = 'sma_slow' , columns = 'sma_fast' , values = 'daily_profit') ,  # Dane
                    labels = dict(x = "Okresy sredniej szybkiej" , y = "Okresy sredniej wolnej" , color = "Profit") ,
                    text_auto = True, # Automatyczne wyświetlanie wartości,
                    width = 570, height = 570,  # Szerokość i wysokość wykresu
                    color_continuous_scale='blues')  # Wybierz inną paletę kolorów, jeśli chcesz
    fig.update_layout(
        title = 'Mapa ciepła profitów dziennych dla różnych kombinacji okresów średnich ruchomych',
        font = dict(
            family = "Arial" ,  # Wybierz rodzaj czcionki
            size = 10 ,  # Wybierz rozmiar czcionki
            color = font_color),  # Wybierz kolor czcionki
        paper_bgcolor = plot_color,  # Ustawienie koloru tła wykresu
        plot_bgcolor = plot_color)  # Ustawienie koloru tła obszaru z wykresem
    # Konwersja wykresu do HTML
    heatmap_html = fig.to_html(full_html = False)


    # Konwersja dataframe do HTML
    table = results_df.to_html(classes = 'table table-bordered')


    # Rysuj wykres liniowy sma_slow, sma_fast dla największego wyniku
    fig = px.line(df_max , y = ['sma1', 'sma2'])
    # Zaktualizuj etykiety dla konkretnych linii i kolor lini dla zmiennej 'c' na czarny
    # fig.update_traces(name = 'Cena', line_color = 'black', selector = dict(name = 'c'))
    fig.update_traces(name = 'SMA Fast' , selector = dict(name = 'sma1'))
    fig.update_traces(name = 'SMA Slow' , selector = dict(name = 'sma2'))
    fig.update_layout(
        title = 'Średnie dla największego profitu.  SMA Fast: ' + str(sm1_max)  + ', SMA Slow:  ' + str(sm2_max),
        font = dict(
            family = "Arial" ,  # Wybierz rodzaj czcionki
            size = 10 ,  # Wybierz rozmiar czcionki
            color = font_color),  # Wybierz kolor czcionki
        xaxis_title='',
        yaxis_title='Cena',
        xaxis_showgrid=False,  # Ukryj linie siatki wzdłuż osi X
        yaxis_showgrid=False,   # Ukryj linie siatki wzdłuż osi Y
        width=1000,             # Szerokość wykresu w pikselach
        height=400,             # Wysokość wykresu w pikselach
        paper_bgcolor = plot_color,  # Ustawienie koloru tła wykresu
        plot_bgcolor = plot_color)  # Ustawienie koloru tła obszaru z wykresem
    # Konwertuj wykres do HTML
    plot_max_html = fig.to_html(full_html = False)


    # Rysuj wykres liniowy sma_slow, sma_fast dla najmniejszego wyniku
    fig = px.line(df_min ,y = ['sma1', 'sma2' ])
    #ig = px.line(df_min ,y = ['c', 'sma1', 'sma2' ])
    # Zaktualizuj etykiety dla konkretnych linii i kolor lini dla zmiennej 'c' na czarny
    # fig.update_traces(name = 'Cena' , selector = dict(name = 'c'))
    fig.update_traces(name = 'SMA Fast' , selector = dict(name = 'sma1'))
    fig.update_traces(name = 'SMA Slow' , selector = dict(name = 'sma2'))
    # Zaktualizuj kolor lini dla zmiennej 'c' na czarny
    # fig.update_traces(line_color = 'black' , selector = dict(name = 'c'))
    fig.update_layout(
        title = 'Średnie dla najmniejszego profitu.  SMA Fast: ' + str(sm1_min)  + ', SMA Slow:  ' + str(sm2_min),
        font = dict(
            family = "Arial" ,  # Wybierz rodzaj czcionki
            size = 10 ,  # Wybierz rozmiar czcionki
            color = font_color),  # Wybierz kolor czcionki
        xaxis_title='',
        yaxis_title='Cena',
        xaxis_showgrid=False,  # Ukryj linie siatki wzdłuż osi X
        yaxis_showgrid=False,   # Ukryj linie siatki wzdłuż osi Y
        width=1000,             # Szerokość wykresu w pikselach
        height=400,             # Wysokość wykresu w pikselach
        paper_bgcolor = plot_color,  # Ustawienie koloru tła wykresu
        plot_bgcolor = plot_color)  # Ustawienie koloru tła obszaru z wykresem
    # Konwertuj wykres do HTML
    plot_min_html = fig.to_html(full_html = False)

    return render_template('charts.html',
                           heatmap=heatmap_html,
                           periods_1 = periods_1,
                           periods_2 = periods_2,
                           plot_max_html=plot_max_html,
                           plot_min_html=plot_min_html,
                           profit_max = profit_max,
                           profit_min = profit_min,
                           daily_profit_max = daily_profit_max,
                           daily_profit_min = daily_profit_min,
                           sm1_max = sm1_max,
                           sm2_max = sm2_max,
                           sm1_min = sm1_min,
                           sm2_min = sm2_min,
                           mpld3=mpld3,
                           table = table,
                           opis = session['opis'])

@app.route('/charts', methods=['POST'])
def save_data():
    if request.method == 'POST':
        instrument_name = request.form.get('instrument')
        save_data(session['filename'], instrument_name, 20, 50, 100, 100, 100, session['data'].iloc[0]['datetime'], session['data'].iloc[-1]['datetime'])
        return f'Dane zapisane dla instrumentu: {instrument_name}'

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
