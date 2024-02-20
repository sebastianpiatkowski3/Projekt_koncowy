# import pandas as pd
#
# # Tworzenie DataFrame z przykładowymi danymi
# data = {'value': [10, 15, 8, 12]}
# df = pd.DataFrame(data)
#
# # Wartość x
# x = 9
#
# # Wybieranie wierszy od 3 do ostatniego
# subset_df = df.iloc[2:]
#
# # Sprawdzenie warunku
# if any(subset_df['value'] > x):
#     print(f"Wiersz, w którym wartość jest większa od {x}: {subset_df[subset_df['value'] > x].index[0]}")
# else:
#     brak_wartosci = True
#     print(f"Brak wartości większych od {x}: {brak_wartosci}")
# from tqdm import tqdm
# import time
#
# for i in tqdm(range(100)):
#     time.sleep(0.01)  # symulacja długotrwałego zadania
#
# import numpy as np
# #  print character number ASCII code from 33 to 126
# for i in range(33, 255):
#     print(f'{i} : {chr(i)}')
# # Przykładowe dane
# data = np.random.normal(size=100)
#
# # Obliczanie histogramu
# hist, bins = np.histogram(data, bins=10)
#
# # Wydrukowanie histogramu
# se = ''
# for i in range(len(hist)):
#     a = f'{bins[i]:.2f} ... {bins[i+1]:.2f}'
#     le = len(f'{bins[i]:.2f} ... {bins[i+1]:.2f} : ')
#     # print(le)
#     # print(f'{bins[i]:.2f} ... {bins[i+1]:.2f} : {chr(93) * hist[i]:<80}')
#     se = str(' ' * (20 - le))
#     print(f'{a}: {se} {chr(130) * hist[i]}')

# ________________________
# import pandas as pd
#
# # Przykładowe dane
# data = {
#     'sma_1': [100, 105, 110, 115, 120],
#     'sma_2': [98, 102, 118, 112, 118]
# }
#
# df = pd.DataFrame(data)
# # Oblicz różnicę między wartościami sma_1 a sma_2
# df['diff'] = df['sma_1'] - df['sma_2']
#
# # Znajdź momenty przecięcia (kiedy diff zmienia znak)
# crossings = (df['diff'].shift(1) > 0) & (df['diff'] < 0)
# print(crossings)
#
# # Wybierz wiersze, w których występuje przecięcie
# moments_of_intersection = df[crossings]
# print(moments_of_intersection)
#
# # Wyświetl indeks wiersza i wartość dla każdego momentu przecięcia
# for index, row in moments_of_intersection.iterrows():
#     print(f"Indeks: {index}, Wartość przecięcia: {row['sma_1']:.2f}")
# ________________________


# import matplotlib.pyplot as plt
# import time
#
# x = [0, 1, 2, 3]
# y = [10, 15, 7, 12]
#
# plt.ion()  # Włącz tryb interaktywny
# for i in range(10):
#     y = [val + 1 for val in y]  # Zmiana danych (symulacja aktualizacji)
#
#     plt.plot(x, y)
#     plt.draw()  # Rysuj wykres
#     plt.pause(1)  # Poczekaj 1 sekundę
#
# plt.ioff()  # Wyłącz tryb interaktywny
# plt.show()
# ____________________________

# import pandas as pd
#
# # Przykładowe dane
# data = {
#     'c': [10, 15, 20, 25, 30, 35, 40]
# }
#
# df = pd.DataFrame(data)
# print(df)
#
# periods = [1, 2, 5, 10]
#
# for period1 in periods:
#     for period2 in periods:
#         if period1 != period2:
#             # Oblicz średnią ruchomą dla obu okresów
#             sma1 = df['c'].rolling(window=period1).mean()
#             sma2 = df['c'].rolling(window=period2).mean()
#
#             # Znajdź momenty przecięcia (kiedy sma1 przecina sma2)
#             crossings_upward = (sma1.shift(1) > sma2.shift(1)) & (sma1 < sma2)
#             crossings_downward = (sma1.shift(1) < sma2.shift(1)) & (sma1 > sma2)
#
#             # Zapisz wyniki do dalszej analizy (np. w innym DataFrame lub pliku)
#             # ...
#
#             print(f"Momenty przecięcia (z góry na dół) dla okresów {period1} i {period2}:")
#             print(df[crossings_upward])
#
#             print(f"\nMomenty przecięcia (z dołu w górę) dla okresów {period1} i {period2}:")
#             print(df[crossings_downward])
#             print('-'*50)
# # ____________________________

# import matplotlib.pyplot as plt
# import numpy as np
#
# # Przykładowe dane
# x = np.random.rand(10)
# y = np.random.rand(10)
# values = np.random.rand(10)
#
# # Generowanie mapy cieplnej
# plt.scatter(x, y, c=values, cmap='viridis', s=100)
# plt.colorbar()
#
# # Konfiguracja osi
# plt.xlabel('Oś X')
# plt.ylabel('Oś Y')
#
# # Wyświetlenie mapy cieplnej
# plt.show()
# # ____________________________


# import pandas as pd
#
# # Inicjalizacja list na wyniki
# results = []
#
# periods_1 = [10, 20, 30]
# periods_2 = [50, 100, 150]
#
# # Pętle obliczeniowe
# for period1 in periods_1:
#     for period2 in periods_2:
#         # Tutaj dodaj swój kod obliczeń, np. ppd, profit_total, sum_crossings
#
#         profit_total = period1 + period2  # Twoje obliczenia
#
#
#         # Dodanie wyników do listy
#         results.append({'sma1': period1, 'sma2': period2, 't_p': profit_total, 's_c' : '123'})
#
# # Utworzenie DataFrame z wynikami
# result_df = pd.DataFrame(results)
#
# # Wyświetlenie DataFrame
# print(result_df)
#
# import seaborn as sns
# import matplotlib.pyplot as plt
#
# # Tworzenie mapy ciepła za pomocą seaborn
# plt.figure(figsize=(10, 8))
# heatmap_data = result_df.pivot(index='sma1', columns='sma2', values='t_p')
#
# sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', linewidths=.5)
# plt.title('Mapa ciepła dla danych')
# plt.show()


# import pandas as pd
#
# # Twój DataFrame
# data = {'c': [16655.0, 16670.0, 16700.0, 16680.0, 16580.0, 16485.0, 16435.0, 16530.0, 16700.0, 16700.0, 16735.0, 16690.0, 16775.0],
#         'crossings_upward': [False, True, False, True, False, True, False, True, False, True, False, True, False],
#         'crossings_downward': [True, False, True, False, True, False, True, False, True, False, True, False, True],
#         'crossings': [True, True, True, True, True, True, True, True, True, True, True, True, True]}
#
# df = pd.DataFrame(data)
#
# # Oblicz różnicę dla kolumny 'c'
# df['c_diff'] = df['c'].diff()
# print(df)
#
# # Zastosuj warunki i pomnóż przez -1
# condition = (df['crossings_upward'].shift(-1) == True) & (df['c'].shift(-1) < df['c'])
# df.loc[condition, 'c_diff'] *= -1
#
# # Wypełnij NaN zerami
# df['c_diff'] = df['c_diff'].fillna(0)
#
# # Wyświetl DataFrame po zapełnieniu NaN zerami
# print(df)

# import pandas as pd
# import plotly.express as px
#
# # Tworzenie DataFrame z danymi
# data = {'Styczeń': [5, 3], 'Luty': [7, 1]}
# df = pd.DataFrame(data, index=['Biały', 'Czerwony'])
#
# # Tworzenie mapy ciepła
# fig = px.imshow(df, labels=dict(x="Miesiąc", y="Kolor", color="Wartość"), color_continuous_scale='blues')
#
# fig.show()
# # ____________________________
#
# import yfinance as yf
#
# # Pobierz dane dla DAX40
# data = yf.download('BTC-USD', start='2024-01-01', end='2024-01-31', interval='1h')
#
# # print data only for row 0 and olny for column 0
# print(data.iloc[0, 5])
# print(data.iloc[0])
# # print olny names of columns
# print(data.columns)
#
# # ____________________________


import yfinance as yf

def get_instrument_name(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        instrument_name = info.get('longName', 'Nazwa nieznana')  # Domyślnie ustawia "Nazwa nieznana", jeśli nie ma dostępnej nazwy
        return instrument_name
    except Exception as e:
        print(f"Błąd: {e}")
        return None

# Przykładowe użycie
symbol = '^NDX'  # Możesz zastąpić tym interesującym cię symbolem
instrument_name = get_instrument_name(symbol)

if instrument_name:
    print(f'Nazwa instrumentu dla {symbol}: {instrument_name}')
else:
    print(f'Nie udało się uzyskać nazwy instrumentu dla {symbol}.')
# ____________________________