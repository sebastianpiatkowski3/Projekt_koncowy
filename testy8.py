"""
Działa OK!
"""
import pandas as pd

df = pd.read_csv('GER402.csv', sep=',', header=None)
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

# data = {'candle': [1, 0, 1, 1, 1, 1, 1, 1, 1, 1]}
# df = pd.DataFrame(data)

# print first 10 rows from dataframe
# print(df.head(10))
# print(candle[1])


# Inicjalizujemy zmienne
profit = 0
take_profit = 3
stop_loss = 30
distances = []
distance2 = 0
osiag = []
zakres = 1000
#  print rows from dataframe from 1000 to 1010
print(df.iloc[zakres-10:zakres, :])

def count_profit_long(index, row, df, zakres, profit, take_profit, stop_loss):
    distance2 = 0
    # Iterujemy przez każdy wiersz
    for wiersz in range(index + 1 ,
                        len(df)):  # TODO: for wiersz in range(index+1, # len(df)): # zakres):
        distance2 += 1
        if candle[wiersz] == 1:
            profit += 1
            # print(f'dane z df: {df.iloc[wiersz, 0]}')
        elif candle[wiersz] == 0:
            profit -= 1
        if profit >= take_profit:
            osiag.append(index)
            distance = wiersz - index + 1
            distances.append(distance2)
            profit = 0
            #  exit for loop
            break
        if profit <= -stop_loss:
            # print(f'jestem w   profit <= -stop_loss')
            distances.append('SL')
            profit = 0
            #  exit for loop
            break
        if wiersz == zakres - 1:  # TODO
            # print(f'jestem w   wiersz == len(df)-1')
            distances.append(None)
            profit = 0


# Iterujemy przez każdy wiersz
for index, row in df.iterrows():
    # count_profit_long(index, row, df, zakres, profit, take_profit, stop_loss)
    distance2 = 0
    # Iterujemy przez każdy wiersz
    for wiersz in range(index+1, len(df)): #  TODO: for wiersz in range(index+1, # len(df)): # zakres):
        distance2 += 1
        if candle[wiersz] == 1:
            profit += 1
            # print(f'dane z df: {df.iloc[wiersz, 0]}')
        elif candle[wiersz] == 0:
            profit -= 1
        if profit >= take_profit:
            osiag.append(index)
            distance = wiersz - index + 1
            distances.append(distance2)
            profit = 0
            #  exit for loop
            break
        if profit <= -stop_loss:
            # print(f'jestem w   profit <= -stop_loss')
            distances.append('SL')
            profit = 0
            #  exit for loop
            break
        if wiersz == zakres - 1: # TODO
            # print(f'jestem w   wiersz == len(df)-1')
            distances.append(None)
            profit = 0

print(f'osiag: {osiag}')
print('-'*50)
print(f'distances: {distances}')
print('-'*50)
ilosc_swiec = len(df)
print(f'- skuteczność: {len(osiag)/ilosc_swiec}')
print(f'Balance: {len(osiag)*take_profit - (ilosc_swiec - len(osiag))*stop_loss}')
# Tworzymy DataFrame z wynikami
result_df = pd.DataFrame({'distance': distances})

# Zliczamy ilość wystąpień dla każdej odległości
# result_counts = result_df['distance'].value_counts().sort_index()

# Wyświetlamy wyniki
# print(result_counts)
