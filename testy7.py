"""
Działa OK!
#  describe how the script works
the script iterates through each row of the dataframe
if the candle is 1 then the profit increases by 1
if the candle is 0 then the profit decreases by 1
if the profit is greater than or equal to take_profit then the distance is calculated
the distance is the number of rows from the current row to the  row where the profit is greater than or equal to take_profit
the distance is added to the list distances
the profit is reset to 0
if the profit is less than take_profit then the distance is None
the distance is added to the list distances
the profit is reset to 0
"""
import pandas as pd

# Tworzymy przykładowy DataFrame
data = {'candle': [1, 0, 1, 1, 1, 1, 1, 1, 1, 1]}
df = pd.DataFrame(data)

# Inicjalizujemy zmienne
profit = 0
take_profit = 3
distances = []
distance2 = 0
osiag = []

# Iterujemy przez każdy wiersz
for index, row in df.iterrows():
    distance2 = 0
    # Iterujemy przez każdy wiersz
    for wiersz in range(index+1, len(df)):
        distance2 += 1
        if df['candle'][wiersz] == 1:
            profit += 1
        elif df['candle'][wiersz] == 0:
            profit -= 1
        if profit >= take_profit:
            osiag.append(index)
            distance = wiersz - index + 1
            distances.append(distance2)
            profit = 0
            #  exit for loop
            break
        if wiersz == len(df)-1:
            print(f'jestem w   wiersz == len(df)-1')
            distances.append(None)
            profit = 0

print(f'osiag: {osiag}')
print('-'*50)
print(f'distances: {distances}')
print('-'*50)
ilosc_swiec = len(df)
print(f'- skuteczność: {len(osiag)/ilosc_swiec}')
# Tworzymy DataFrame z wynikami
result_df = pd.DataFrame({'distance': distances})

# Zliczamy ilość wystąpień dla każdej odległości
result_counts = result_df['distance'].value_counts().sort_index()

# Wyświetlamy wyniki
print(result_counts)
