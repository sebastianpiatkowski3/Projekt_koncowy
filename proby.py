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

import pandas as pd

# Przykładowe dane
data = {
    'c': [10, 15, 20, 25, 30, 35, 40]
}

df = pd.DataFrame(data)
print(df)

periods = [1, 2, 5, 10]

for period1 in periods:
    for period2 in periods:
        if period1 != period2:
            # Oblicz średnią ruchomą dla obu okresów
            sma1 = df['c'].rolling(window=period1).mean()
            sma2 = df['c'].rolling(window=period2).mean()

            # Znajdź momenty przecięcia (kiedy sma1 przecina sma2)
            crossings_upward = (sma1.shift(1) > sma2.shift(1)) & (sma1 < sma2)
            crossings_downward = (sma1.shift(1) < sma2.shift(1)) & (sma1 > sma2)

            # Zapisz wyniki do dalszej analizy (np. w innym DataFrame lub pliku)
            # ...

            print(f"Momenty przecięcia (z góry na dół) dla okresów {period1} i {period2}:")
            print(df[crossings_upward])

            print(f"\nMomenty przecięcia (z dołu w górę) dla okresów {period1} i {period2}:")
            print(df[crossings_downward])
            print('-'*50)
# ____________________________


