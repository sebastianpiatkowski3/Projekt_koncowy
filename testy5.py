#  write docstring
"""
This script read data from csv file
The third column is open price
The sixth column is close price
If close price > open price then candle = 1 else candle = 0
Add candle to dataframe
For each candle takes candle and next 6 candles. It should be 7 candles like this: 0,1,0,1,1,0,1
Counts each type of combination of 7 candles and save to csv file with: combination, count
"""

#  Import from DAX40_5pips.csv file to pandas dataframe
import pandas as pd


df = pd.read_csv('test_DAX40_5pips.csv', sep=',', header=None)
#  name column with data as:
date, time, open_price, high, low, close, volume = df.iloc[:, 0], df.iloc[:, 1], df.iloc[:, 2], df.iloc[:, 3], df.iloc[:, 4], df.iloc[:, 5], df.iloc[:, 6]
#  if close > open then candle = 1 else candle = 0
candle = []
for i in range(0, len(open_price)):
    if close[i] > open_price[i]:
        candle.append(1)
    else:
        candle.append(0)
#  add candle to dataframe
df['candle'] = candle

# for each candle take candle and next 6 candles. It should be 7 candles like this: 0,1,0,1,1,0,1
#  count each type of combination of 7 candles and save to csv file with: combination, count

# print first 10 rows from dataframe
print(df.head(10))

# Tworzymy listę stringów
strings = []
for i in range(len(df)-6):
    string = ','.join(map(str, df['candle'][i:i+7]))
    strings.append(string)

# Tworzymy słownik, w którym będą przechowywane pary (string : ilość wystąpień)
counter_strings = {}

# Dla każdego stringa z listy strings
for string in strings:
    # Jeżeli string nie wystąpił wcześniej, dodajemy go do słownika z wartością 1
    if string not in counter_strings:
        counter_strings[string] = 1
    # Jeżeli string już wystąpił wcześniej, zwiększamy jego wartość o 1
    else:
        counter_strings[string] += 1

# Wyświetlamy wynik
print(counter_strings)

#  sort dictionary by values
counter_strings = dict(sorted(counter_strings.items() , key=lambda item: item[1] , reverse=True))
for key, value in enumerate(counter_strings.items()):
    print(key, value)



# print('-'*50)
# print(type(counter_strings))
# #  save dictionary to csv file
# import csv
# file_name = 'counter' + str(7) + '_counter.csv'
# # Otwieramy plik CSV w trybie zapisu
# with open_price(file_name, 'w', newline= '') as csvfile:
#     # Tworzymy obiekt writer, który pozwala nam zapisywać wiersze do pliku CSV
#     writer = csv.writer(csvfile)
#
#     # Dla każdej pary klucz:wartość w słowniku
#     for klucz, wartosc in counter_strings.items():
#         # Zapisujemy parę klucz:wartość jako wiersz do pliku CSV
#         writer.writerow([klucz, wartosc])


