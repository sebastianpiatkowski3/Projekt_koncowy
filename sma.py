"""
Ten kod najpierw wczytuje dane z pliku ‘ger.csv’, a następnie przechodzi przez każdy wiersz w ramce danych. Jeżeli wartość w kolumnie ‘t’ jest większa od zera, oblicza ‘tp’ i szuka pierwszej wartości w następnych wierszach, która jest równa lub większa od ‘tp’. Następnie oblicza różnicę czasu między tymi dwoma wierszami i dodaje ją do listy ‘czasy’. Jeżeli wartość w kolumnie ‘t’ jest mniejsza od zera, proces jest analogiczny, ale szuka pierwszej wartości, która jest równa lub mniejsza od ‘tp’.
co robi ten kod:
if df.loc[j, ['o', 'h', 'l', 'c']].ge(tp).any():
Ten fragment kodu sprawdza, czy jakakolwiek wartość w kolumnach ‘o’, ‘h’, ‘l’, ‘c’ w danym wierszu (indeksowanym przez ‘j’) jest większa lub równa wartości ‘tp’.
Funkcja df.loc[j, ['o', 'h', 'l', 'c']] zwraca wartości z kolumn ‘o’, ‘h’, ‘l’, ‘c’ dla wiersza o indeksie ‘j’.
Funkcja ge(tp) (greater than or equal to) porównuje te wartości z ‘tp’ i zwraca wartości logiczne (True lub False) dla każdej z nich.
Funkcja any() zwraca True, jeśli jakakolwiek wartość w wyniku jest True (czyli jeśli jakakolwiek wartość w kolumnach ‘o’, ‘h’, ‘l’, ‘c’ jest większa lub równa ‘tp’), a w przeciwnym razie zwraca False.
Więc cały ten fragment kodu jest używany do znalezienia pierwszego wiersza, w którym jakakolwiek wartość w kolumnach ‘o’, ‘h’, ‘l’, ‘c’ jest większa lub równa ‘tp’.
W tym kodzie, jeśli dla danego wiersza nie zostanie znaleziona żadna wartość spełniająca warunek, do listy ‘czasy’ zostanie dodana wartość ‘Nie znaleziono wartości spełniającej warunek’.
W powyższym kodzie, idxmax() zwraca nazwę kolumny, w której warunek jest spełniony. Ta nazwa kolumny jest następnie dodawana do listy czasy. Pamiętaj, że idxmax() zwróci nazwę pierwszej kolumny, która spełnia warunek, jeśli istnieje więcej niż jedna taka kolumna.
W powyższym kodzie, zmienna max_h jest inicjalizowana wartością df.loc[i, 'h'] przed rozpoczęciem pętli. Następnie, w każdym przejściu pętli, max_h jest aktualizowane do największej wartości spośród max_h i df.loc[j, 'h']. Ta największa wartość jest następnie dodawana do listy czasy. Pamiętaj, że ta metoda zwróci największą wartość df.loc[j, 'h'] dla wszystkich j od i+1 do len(df), które spełniają warunek if condition.any().
"""
# TODO: 1. obsłużyć take_profit < 0, czyli grę na shorty
# TODO: 2. liczyć MA20 i MA50, wykryć trend i grać tylko w kierunku trendu
import time

start = time.process_time()

import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import sys

file = ('GER402Renko5.csv')
#file = 'GER40_2024_ohlc.csv'
# file = 'NQ100_10pips_ohlc.csv'
# file = 'GER40_20240124ohlc.csv'
# file = 'ohlcNQ100_5pips.csv'
# file = 'GERMANY402ohlc.csv'
# Wczytaj dane z pliku csv
# df = pd.read_csv(file)

# Czy liczyć drugą średnią kroczącą?
druga_srednia = True
"""
czy liczyć drugą średnią kroczącą:
- jeżeli nie to liczę na podstawie 'c', 
- jeżeli tak to na podstawie 'sma1' i 'sma2'
"""

# Lista z nazwami kolumn
nazwy_kolumn = ['d', 'g', 'o', 'h', 'l', 'c', 'w']

# Utwórz pustą ramkę danych z nazwami kolumn
#df = pd.DataFrame(columns=nazwy_kolumn)

df = pd.read_csv(file , sep = ',' , header = None, names=nazwy_kolumn)
#d, g, o, h, l, c, w = df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2], df.iloc[:, 3], df.iloc[:, 4], df.iloc[:, 5], df.iloc[:, 6]
print(df)
df['datetime'] = pd.to_datetime(df['d'] + ' ' + df['g'])
time_difference = df.iloc[-1]['datetime'] - df.iloc[0]['datetime']

print(df)


def kombinuj_okresy_ma(df):
    momenty = []
    ind = 0
    pips_per_day_df = pd.DataFrame(columns = ['sma1' , 'sma2' , 'ppd' , 'p_t' , 's_c'])
    # ppd = pips per day, p_t = profit_total, s_c = sum_crossings
    periods_1 = [10, 20]#, 20 , 30 , 45 , 70 , 100]
    periods_2 = [50, 100, 150]

    for period1 in periods_1:
        for period2 in periods_2:
            if period1 != period2:

                # Oblicz średnią ruchomą:
                sma1 = df['c'].rolling(window = period1).mean()
                df['sma1'] = sma1

                if druga_srednia:
                    sma2 = df['c'].rolling(window = period2).mean()
                    df['sma2'] = sma2
                else:
                    sma2 = df['c']
                    df['sma2'] = sma2


                # Znajdź momenty przecięcia (kiedy sma1 przecina sma2)
                crossings_upward = (sma1.shift(1) > sma2.shift(1)) & (sma1 < sma2) # cena spada:  sprzedaj
                crossings_downward = (sma1.shift(1) < sma2.shift(1)) & (sma1 > sma2) # cena rosnie: kupuj
                # Dodaj kolumnę 'crossings_upward' do ramki danych
                df['crossings_upward'] = crossings_upward
                df['crossings_downward'] = crossings_downward

                crossings_df = df[df['crossings_upward'] | df['crossings_downward']].copy()
                df['crossings'] = crossings_df['crossings_upward'] | crossings_df['crossings_downward']
                df['crossings'].fillna(False , inplace = True)
                print(f'df: \n{df[16:25]}')
                momenty = df[df['crossings'].copy()]
                momenty_print = momenty[[ 'c' , 'crossings_upward', 'crossings_downward', 'crossings']]
                print(f'momenty: \n{momenty_print}')
                diffs = momenty['c'].diff()  # tu  liczę różnice, czyli profit
                
                print(f'diffs: \n{diffs[0:15]}')
                # sum all absolute values of data from the second column of diffs
                profit_total = diffs.abs().sum()
                print(f'- Profit total: {profit_total:.1f}')
                ppd = round(profit_total / time_difference.days , 1)
                sum_crossings = len(diffs)

                if not druga_srednia:
                    period2 = 'close'
                new_row = {'sma1': period1 , 'sma2': period2 , 'ppd': ppd}
                pips_per_day_df.loc[ind] = [period1 ,
                                            period2 , ppd ,
                                            profit_total ,
                                            sum_crossings]
                ind += 1

                print(f'- Pips per day: {ppd}')
                print(f'- ilosć crossów: {len(diffs)}')
                print(f'- Time_difference: {time_difference}')
                print(pips_per_day_df)
                # sys.exit()

                print('-' * 50)


kombinuj_okresy_ma(df)
# sys.exit()


# Twórz wykres
plt.plot(df['sma1'] , label = 'sma1')
# plt.plot(df['c_mb'], label='c_mb')
plt.plot(df['c'] , label = 'c')
# plt.scatter(moments_of_intersection_upward.index , moments_of_intersection_upward['c_ma'] , color = 'r' , marker = 'o' , label = 'Przecięcie (góra-dół)')
# plt.scatter(moments_of_intersection_downward.index , moments_of_intersection_downward['c_mb'] , color = 'g' , marker = 'x' , label = 'Przecięcie (dół-góra)')
plt.xlabel('Indeks')
plt.ylabel('Wartość')
plt.title('Wykres danych c_ma i c_mb z momentami przecięcia')
plt.legend()
plt.show()

# Tworzymy wykres liniowy z kolumny 'c' i jej średniej ruchomej
# plt.plot(df['c'], label='c')
# plt.plot(df['c_ma'], label='c_ma')
# plt.plot(df['c_mb'], label='c_mb')

# Dodajemy legendę i etykiety osi
# plt.legend()
# plt.xlabel('Indeks')
# plt.ylabel('Wartość')
#
# # Pokazujemy wykres
# plt.show()
sys.exit()

# ma_fast = df['o'].rolling(window=10).mean()
# print(ma_fast)
# # Obliczamy średnią kroczącą z 3 okresów dla kolumny y
# df['c_ma'] = df['c'].rolling(10).mean()
#
# # Tworzymy wykres liniowy z kolumny y i jej średniej kroczącej
# plt.plot(df['c'], df['c'], label='c')
# plt.plot(df['x'], df['c_ma'], label='c_ma')
# # Tworzymy wykres liniowy z kolumn x i y dataframe
# plt.plot(ma_fast.iloc[1], df['c'])
# # Pokazujemy wykres
# plt.show()


sys.exit()
# Zamień kolumnę 'g' na format daty i czasu
# df['g'] = pd.to_datetime(df['g'] , format = '%H:%M')


czasy = []
notfound = 0
max_h = 0
min_h = 0
a = 8
stop_loss = 0  # dodatnia wartość
sum_stop_loss = 0
profit = 0
spread = 0
direction = []
# Inicjalizujemy pustą listę wyników
results = []
trend = 0
trend_level = 0
najwiekszy_fpm = 0


def count_trend(df):
    fast = 10
    slow = 50
    # count moving average 20 and 50
    # count moving average(20):
    ma_fast = df['o'].rolling(window = fast).mean()
    ma_slow = df['o'].rolling(window = slow).mean()
    # if ma20 > ma50 then trend = 1
    # if ma20 < ma50 then trend = -1
    return ma_fast , ma_slow


# ma_slow = count_trend(df)[0] # wektor ze średnimi kroczącymi
# ma_fast = count_trend(df)[1] # wektor ze średnimi kroczącymi
# print(ma_slow[51], ma_fast[51])


values_a = range(15 , 16)
values_b = range(0 , 1)
for a in values_a:
    for stop_loss in values_b:
        stop_loss = 50
        czasy = []
        notfound = 0
        max_h = 0
        min_h = 0
        sum_stop_loss = 0
        profit = 0
        take_profit_count = 0
        spread = 1
        direction = []

        trend = 0
        trend_level = 0
        # Przejdź przez każdy wiersz w ramce danych
        for i in tqdm(range(len(df))):
            # a = df.loc[i , 't']
            # trend = ma_fast[i] - ma_slow[i] # trend w chwili 'i'

            # a = 0
            # if trend > 15:
            #     a = aa
            direction.append(df.loc[i , 'c'] - df.loc[i , 'o'])
            found = False
            if a > 0:
                tp = df.loc[i , 'o'] + a
                sl = df.loc[i , 'o'] - stop_loss  # stop loss = cena otwarcia - stop_loss np. 16685.0
                min_h = df.loc[i , 'h']  # Inicjalizacja zmiennej min_h
                min_sl = df.loc[i , 'l']  # zawsze najniższa napotkana wartość w celu wyłapania stop_loss
                for j in range(i + 1 , len(df)):
                    condition = df.loc[j , ['o' , 'h' , 'l' , 'c']].ge(tp)
                    fpm = df.loc[i , 'o'] - df.loc[j , 'o']  # fpm = first price movement
                    najwiekszy_fpm = max(najwiekszy_fpm , fpm)
                    # if i < 4:
                    #     print(f'condition: {condition}')
                    min_h = min(min_h , df.loc[j , 'l'])  # Aktualizacja zmiennej max_h
                    min_sl = min(min_sl , df.loc[j , 'l'])
                    if condition.any():
                        take_profit_count += 1
                        # column_name = condition.idxmax()  # Zwraca nazwę kolumny, w której warunek jest spełniony
                        # true_indices = condition[condition].index
                        # if i < 4:
                        #     print("Indeksy spełniające warunek:" , true_indices)
                        # czas = (df.loc[j , 'g'] - df.loc[i , 'g']).total_seconds() / 60
                        odleglosc = j - i
                        min_h = min_h - df.loc[i , "o"]
                        czasy.append(
                            f'{df.loc[i , "o"]}, ___ {j} ___ , {tp}, ___ , odlegloc: {odleglosc}, min_h: {min_h}')
                        found = True
                        profit += a - spread
                        break
                    if min_sl < sl:  # czy ten warunek jest dobry?? jak wyłapać stop_lossy?
                        # print(f'--- jestem w min_sl < sl: {min_sl} < {sl}, open: {df.loc[i , 'o']}, i: {i}, j: {j}')
                        found = False
                        sum_stop_loss += 1
                        break
            elif a < 0:
                tp = df.loc[i , 'o'] + a
                max_h = df.loc[i , 'h']  # Inicjalizacja zmiennej max_h
                for j in range(i + 1 , len(df)):
                    condition = df.loc[j , ['o' , 'h' , 'l' , 'c']].le(tp)
                    max_h = max(max_h , df.loc[j , 'h'])  # Aktualizacja zmiennej max_h
                    if condition.any():
                        column_name = condition.idxmax()  # Zwraca nazwę kolumny, w której warunek jest spełniony
                        # czas = (df.loc[j , 'g'] - df.loc[i , 'g']).total_seconds() / 60
                        max_h = max_h - df.loc[i , "o"]
                        czasy.append(
                            f'{df.loc[i , "o"]}, ___ {a} ___ , {tp}, ___ , kolumna: {column_name}, max_h: {max_h}')
                        # max_h = df.loc[i , "o"] - max_h
                        found = True
                        profit += -a + spread
                        if max_h < stop_loss:
                            found = False
                        break
            if not found:
                notfound += 1
                czasy.append(f'Nie znaleziono wartości spełniającej warunek, min_sl: {min_sl}, min_h: {min_h}')

        # for value in enumerate(czasy):
        #     print(value)

        print(f'najwiekszy_fpm: {najwiekszy_fpm}')
        print(f'ilosć swiec: {len(df)}')
        print(f'sum_stop_loss: {sum_stop_loss}')
        print(f'notfound: {notfound}')
        print(f'take_profit_count: {take_profit_count}')
        print(f'profit: {profit}')
        loss = notfound * (stop_loss + spread)
        print(f'loss: {loss}')
        print('-' * 70)
        print(file)
        balance = profit - loss
        print(f'BALANCE: {balance} for take profit: {a} and stop loss: {stop_loss}')
        print('-' * 70)
        #  print unique values from list direction and sum of each value
        # print({x: direction.count(x) for x in direction})
        dict = {x: direction.count(x) for x in direction}
        for key , value in dict.items():
            print(f'{key}: {value}')

        end = time.process_time()
        execution_time = end - start
        print(f"Czas wykonania: {execution_time} sekund")
        print(f'ilosć swiec: {len(df)}')
        results.append((a , stop_loss , balance , notfound , sum_stop_loss , profit , loss , execution_time))
        print(f'results: {results}')
        # Tworzymy DataFrame z wynikami
df_results = pd.DataFrame(results ,
                          columns = ['take_profit' , 'stop_loss' ,
                                     'balance' , 'notfound' ,
                                     'sum_stop_loss' , 'profit' ,
                                     'loss' , 'execution_time'])

print(df_results)


def save_results(df_results):
    # Zapisujemy DataFrame do pliku CSV
    file_result = 'wyniki_kombinacji_tp_sl' + file + '.csv'
    df_results.to_csv(file_result , index = False)
    print(f"Wyniki zostały zapisane do {file_result}.")


def draw_plot(df_results):
    df = pd.DataFrame(df_results)

    # Tworzymy macierz danych do mapy ciepła
    heatmap_data = df.pivot_table(index = 'stop_loss' ,
                                  columns = 'take_profit' , values = 'balance')

    # Ustawienie stylu tła na ciemny
    sns.set_style("darkgrid")

    # Tworzymy mapę ciepła
    plt.figure(figsize = (8 , 6))
    sns.heatmap(heatmap_data , annot = True , cmap = 'Blues' ,
                linewidths = 0.5 , fmt = '.0f')  # , vmin = 0 , vmax = 200)

    # Dodajemy tytuł i etykiety osi
    plt.title(f"Mapa ciepła: Balance dla: {file}")
    plt.xlabel("Take Profit")
    plt.ylabel("Stop Loss")

    #     saves a plot to a file
    file_plot = 'mapa_ciepla' + file + '.png'
    plt.savefig(file_plot)
    print(f'Wykres został zapisany do pliku: {file_plot}')
    # Wyświetlamy wykres
    plt.show()


save_results(df_results)

draw_plot(df_results)



