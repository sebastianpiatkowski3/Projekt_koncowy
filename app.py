from typing import Any

from flask import Flask, render_template, request, g, session
from pandas import DataFrame

from flask_session import Session
import plotly.express as px
import pandas as pd
import mpld3
import yfinance as yf
from pandas.errors import ParserError
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache

app = Flask(__name__)

app.config["SECRET_KEY"] = "psnt"  # Klucz prywatny aplikacji dla celów m.in. bezpieczeństwa
app.config['SESSION_TYPE'] = 'filesystem'
app_info = {'db_file' : r'C:\Users\sebas\PycharmProjects\Currency\profits.db'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profits.db'
db = SQLAlchemy(app)
Session(app)

# Inicjalizacja rozszerzenia pamięci podręcznej
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

data = None

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
        new_profit = Profits(file=file,
                             instrument=instrument,
                             sma_slow=sma_slow,
                             sma_fast=sma_fast,
                             daily_profit=daily_profit,
                             total_profit=total_profit,
                             crossover_sum=crossover_sum,
                             start_date=start_date,
                             end_date=end_date)
        db.session.add(new_profit)
        db.session.commit()
        return new_profit.id
    except Exception as e:
        print(f"Błąd: {e}")
        return None

def check_csv(df):
    error_text = ''
    # Sprawdź liczbę kolumn
    if len(df.columns) == 7:
        # Sprawdź, czy pierwsza kolumna to data
        if pd.api.types.is_datetime64_any_dtype(df.iloc[: , 0]):
            # Sprawdź, czy druga kolumna to godzina
            if pd.api.types.is_datetime64_any_dtype(df.iloc[: , 1]):
                error_text += ("Plik CSV spełnia warunki.")
            else:
                error_text += ("Druga kolumna nie zawiera godziny.")
        else:
            error_text += ("Pierwsza kolumna nie zawiera daty.")
    else:
        error_text += ("Plik CSV nie zawiera 7 kolumn.")

    # Lista numerów kolumn do sprawdzenia (kolumny są indeksowane od 0)
    numery_kolumn = [2 , 3 , 4 , 5 , 6]
    # Sprawdź, czy kolumny zawierają liczby
    for numer_kolumny in numery_kolumn:
        kolumna = df.iloc[: , numer_kolumny]
        try:
            pd.to_numeric(kolumna , errors = 'raise')
        except ValueError:
            error_text += (f"Kolumna {numer_kolumny + 1} nie zawiera liczb.")
    return error_text

def read_data(file):
    try:
        # Lista z nazwami kolumn
        nazwy_kolumn = ['Date', 'time', 'Open', 'High', 'Low', 'Close', 'Volume']
        # Wczytaj dane z pliku CSV
        df = pd.read_csv(file , sep = ',' , header = None, names=nazwy_kolumn)
        error_text = check_csv(df)
        if error_text:
            pass # TODO
        df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['time']) # Połącz kolumny 'Date' i 'time' w jedną kolumnę 'Datetime'
        df = df.drop(columns = 'Date')  # Usuń kolumnę 'Date'
        df = df.drop(columns = 'time')  # Usuń kolumnę 'time'
        df = df[[df.columns[-1]] + list(df.columns[:-1])]  # Przenieś kolumnę 'Datetime' na pierwsze miejsce
        return df
    except ParserError as e:
       g.flash_message = f"Błąd konwersji danych: {e}. Sprawdź format danych i spróbuj ponownie."
       return None


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
    return df['Close'].rolling(window=period).mean()

def find_crossings(df, sma_fast, sma_slow):
    crossings_upward = (sma_fast.shift(1) > sma_slow.shift(1)) & (sma_fast < sma_slow)
    crossings_downward = (sma_fast.shift(1) < sma_slow.shift(1)) & (sma_fast > sma_slow)
    return crossings_upward, crossings_downward

def apply_conditions(momenty):
    condition = (momenty['crossings_upward'].shift(-1) == True) & (momenty['Close'].shift(-1) < momenty['Close'])
    momenty.loc[condition, 'close_diff'] *= -1
    momenty.loc[:, 'close_diff'] = momenty['close_diff'] - 1

def calculate_profits(diffs, time_difference):
    total_profit = round(diffs.sum(), 0)
    interval = time_difference
    daily_profit = round(total_profit / interval, 1)  # Oblicz profit na godzinę
    daily_profit = round(daily_profit * 24, 1)  # Przelicz na dobę
    return total_profit, daily_profit

periods_1 = [5, 10 , 20 , 30, 45 , 70 , 100]
periods_2 = [20, 30, 50 , 100, 150, 200, 250, 300]

def count_crossings(df, source='', instrument_name=''):
    df_copy = df.copy()
    results = []
    profit_max = float('-inf')
    profit_min = float('inf')
    daily_profit_max = float('-inf')
    daily_profit_min = float('inf')
    sma_fast_max = float('-inf')
    sma_slow_max = float('-inf')
    sma_fast_min = float('inf')
    sma_slow_min = float('inf')

    for period1 in periods_1:
        for period2 in periods_2:
            if period1 < period2:
                sma_fast = calculate_sma(df_copy, period1)
                df_copy['sma_fast'] = sma_fast
                sma_slow = calculate_sma(df_copy, period2)
                df_copy['sma_slow'] = sma_slow

                crossings_upward, crossings_downward = find_crossings(df_copy, sma_fast, sma_slow)

                df_copy['crossings_upward'] = crossings_upward
                df_copy['crossings_downward'] = crossings_downward

                df_copy['crossings'] = df_copy['crossings_upward'] | df_copy['crossings_downward']
                df_copy.fillna({'crossings': False}, inplace=True)

                momenty = df_copy[df_copy['crossings']]

                momenty.loc[:, 'close_diff'] = momenty['Close'].diff()
                momenty.loc[:, 'close_diff'] = momenty['close_diff'].fillna(0)

                apply_conditions(momenty)

                diffs = momenty['close_diff']

                if len(df_copy) >= 2:
                    time_difference = df_copy.iloc[-1]['Datetime'] - df_copy.iloc[0]['Datetime']
                    # Kontynuuj z obliczeniami
                else:
                    # Obsłuż sytuację, gdy DataFrame ma mniej niż dwa wiersze
                    print("DataFrame ma zbyt mało wierszy.")
                # count difference between date in hours
                time_difference = time_difference.total_seconds() / 3600  # Convert to hours
                time_difference_days = round(time_difference / 24, 0) # Convert to days
                total_profit, daily_profit = calculate_profits(diffs, time_difference)

                crossover_sum = len(diffs)
                results.append({'sma_slow': period1, 'sma_fast': period2, 'daily_profit': daily_profit,
                                'total_profit': total_profit, 'crossover_sum': crossover_sum})

                if total_profit > profit_max:
                    profit_max = total_profit
                    daily_profit_max = daily_profit
                    sma_fast_max = period1
                    sma_slow_max = period2
                    df_max = df_copy.copy()
                if total_profit < profit_min:
                    profit_min = total_profit
                    daily_profit_min = daily_profit
                    sma_fast_min = period1
                    sma_slow_min = period2
                    df_min = df_copy.copy()
    # save data to database
    save_data(source, instrument_name, sma_slow_max, sma_fast_max, daily_profit_max, profit_max, len(diffs), df_max.iloc[0]['Datetime'], df_max.iloc[-1]['Datetime'])
    return (results,
            profit_max,
            profit_min,
            daily_profit_max,
            daily_profit_min,
            sma_fast_max,
            sma_slow_max,
            sma_fast_min,
            sma_slow_min,
            df_max,
            df_min,
            time_difference_days)

opis = ''


@app.route('/index' , methods = ['GET' , 'POST'])
def index():
    # Inicjalizacja sesji
    session.setdefault('data' , None)
    session.setdefault('outcome' , None)
    session.setdefault('results_df' , None)
    session.setdefault('opis' , '')
    session.setdefault('filename' , '')

    if request.form:
        # Sprawdź, który przycisk został naciśnięty
        if 'submit_data' in request.form:
            session.clear()  # Przed wczytaniem nowych danych wyczyść sesję
            # Pobierz dane z formularza
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            instrument = request.form.get('ticker')
            timeframe = request.form.get('timeframe')
            # Pobierz dane z yfinance
            data = yf.download(instrument , start = start_date , end = end_date , interval = timeframe)
            data.reset_index(inplace = True)  # remove index 'Datetime'
            data = data.drop(columns = 'Adj Close')  # Usuń kolumnę 'Adj Close'
            # Pobierz 10 pierwszych wierszy danych
            data_10 = data.head(10) if data is not None else ''
            session['data'] = data  # Zapisz dane w sesji
            nazwa_instrumentu = get_instrument_name(instrument)
            session['opis'] = f'Dane dla {nazwa_instrumentu} w okresie od {start_date} do {end_date} z interwałem {timeframe}.'
            outcome_count_crossings = count_crossings(data , 'API' , nazwa_instrumentu)
            session['results_df'] = pd.DataFrame(outcome_count_crossings[0])
            session['outcome'] = outcome_count_crossings
        if 'submit_file' in request.form:
            session.clear()  # Przed wczytaniem nowych danych wyczyść sesję
            csv_file = request.files['csv']
            session['filename'] = csv_file.filename
            filename = session.get('filename' , '')
            data: DataFrame | None | Any = read_data(csv_file)
            print(f'=*' * 50)
            print(f'data 265: {data}')
            print(f'=*' * 50)
            print(f'=*' * 50)
            # Pobierz 10 pierwszych wierszy danych
            data_10 = data.head(10) if data is not None else ''
            outcome_count_crossings = count_crossings(data , 'CSV' , filename)
            print(f'=*'*50)
            print(f'data 272: {data}')
            print(f'=*' * 50)
            print(f'=*' * 50)
            session['data'] = data  # Zapisz dane w sesji
            session['outcome'] = outcome_count_crossings
            session['opis'] = f'Dane z pliku: {filename}'

    # Sprawdź, czy 'opis' istnieje w sesji przed użyciem
    session['opis'] = session.get('opis' , '')

    if session['data'] is not None:
        data_10 = session['data'].head(10)
    else: data_10 = data.head(10) if data is not None else ''
    if not data_10.empty:
        data_html = data_10.to_html(classes = 'table table-bordered')
    else:
        data_html = ''

    return render_template('index.html' ,
                           data_html = data_html ,
                           outcome = session['outcome'] ,
                           opis = session['opis'] ,
                           filename = session.get('filename' , ''))


@app.route('/charts')
# @cache.cached(timeout=180)  # Cache na 60 sekund
def charts():
    outcome = session['outcome']
    if outcome is not None:
        results_df = pd.DataFrame(outcome[0])
        profit_max = outcome[1]
        profit_min = outcome[2]
        daily_profit_max = outcome[3]
        daily_profit_min = outcome[4]
        sm1_max = outcome[5]
        sm2_max = outcome[6]
        sm1_min = outcome[7]
        sm2_min = outcome[8]
        df_max = outcome[9]
        df_min = outcome[10]
        time_difference_days = str(outcome[11])

        plot_color = '#1F1F1F'
        font_color = '#D3D3D3'
        # Rysowanie mapy ciepła
        # Przekształć 'sma_fast' i 'sma_slow' na łańcuchy znaków
        results_df['sma_slow'] = results_df['sma_slow'].astype(str)
        results_df['sma_fast'] = results_df['sma_fast'].astype(str)
        # Przekształć 'sma_fast' i 'sma_slow' na typ kategorialny z odpowiednią kolejnością
        # Tworzenie listy unikalnych wartości z kolumny 'sma_fast'
        unique_values_sma_fast =  results_df['sma_slow'].unique()  # czyli:   sma_fast_order = ['20' , '30' , '50' , '100']  # Ustal odpowiednią kolejność
        unique_values_sma_slow =  results_df['sma_fast'].unique()
        results_df['sma_slow'] = pd.Categorical(results_df['sma_slow'] , categories = unique_values_sma_fast , ordered = True)
        results_df['sma_fast'] = pd.Categorical(results_df['sma_fast'] , categories = unique_values_sma_slow , ordered = True)
        """    W Plotly Express, funkcja imshow() domyślnie tworzy komórki o równej wielkości. Jeśli zauważasz, że komórki mają różne rozmiary, może to wynikać z tego, że wartości ‘sma_fast’ i ‘sma_slow’ są używane jako numeryczne indeksy, a nie jako kategorie.
    Jednakże, jeśli twoje dane ‘sma_fast’ i ‘sma_slow’ są rzeczywiście numeryczne i chcesz je przedstawić jako kategorie, możesz spróbować przekształcić te wartości na łańcuchy znaków.
    W powyższym kodzie, results_df['sma_fast'].astype(str) i results_df['sma_slow'].astype(str) przekształcają ‘sma_fast’ i ‘sma_slow’ na łańcuchy znaków. Dzięki temu, każda unikalna wartość ‘sma_fast’ i ‘sma_slow’ jest traktowana jako osobna kategoria, a nie jako liczba, co powinno sprawić, że wszystkie komórki na mapie ciepła będą miały tę samą wielkość."""
        """    Przekształca DataFrame results_df tak,
        że kolumny i indeksy są określone przez wartości ‘sma_fast’ i ‘sma_slow’,
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
        fig = px.line(df_max , y = ['sma_fast', 'sma_slow'])
        # Zaktualizuj etykiety dla konkretnych linii i kolor lini dla zmiennej 'Close' na czarny
        # fig.update_traces(name = 'Cena', line_color = 'black', selector = dict(name = 'Close'))
        fig.update_traces(name = 'SMA Fast' , selector = dict(name = 'sma_fast'))
        fig.update_traces(name = 'SMA Slow' , selector = dict(name = 'sma_slow'))
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
        fig = px.line(df_min ,y = ['sma_fast', 'sma_slow' ])
        #ig = px.line(df_min ,y = ['Close', 'sma_fast', 'sma_slow' ])
        # Zaktualizuj etykiety dla konkretnych linii i kolor lini dla zmiennej 'Close' na czarny
        # fig.update_traces(name = 'Cena' , selector = dict(name = 'Close'))
        fig.update_traces(name = 'SMA Fast' , selector = dict(name = 'sma_fast'))
        fig.update_traces(name = 'SMA Slow' , selector = dict(name = 'sma_slow'))
        # Zaktualizuj kolor lini dla zmiennej 'Close' na czarny
        # fig.update_traces(line_color = 'black' , selector = dict(name = 'Close'))
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
                               time_difference_days = time_difference_days,
                               mpld3=mpld3,
                               table = table,
                               opis = session['opis'])
    else:
        komunikat = "Nie wybrano jeszcze danych do analizy."
        return render_template('charts.html',
                               heatmap_html = komunikat,
                                periods_1 = komunikat,
                                periods_2 = komunikat,
                                plot_max_html = komunikat,
                                plot_min_html = komunikat,
                                profit_max = komunikat,
                                profit_min = komunikat,
                                daily_profit_max = komunikat,
                                daily_profit_min = komunikat,
                                sm1_max = komunikat,
                                sm2_max = komunikat,
                                sm1_min = komunikat,
                                sm2_min = komunikat,
                                time_difference_days = komunikat,
                                mpld3 = komunikat,
                                table = komunikat,
                                opis = komunikat,
                                )

@app.route('/profits')
def profits():
    get_profits = Profits.query.order_by(Profits.daily_profit.desc()).all()
    return render_template('profits.html', profits=get_profits)

# @app.route('/charts', methods=['POST'])
# def save_data_manually():
#     if request.method == 'POST':
#         instrument_name = request.form.get('instrument')
#         save_data(session['filename'], instrument_name, 20, 50, 100, 100, 100, session['data'].iloc[0]['Datetime'], session['data'].iloc[-1]['Datetime'])
#         return f'Dane zapisane dla instrumentu: {instrument_name}'

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
