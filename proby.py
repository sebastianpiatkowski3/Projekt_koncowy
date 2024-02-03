import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# # Przykładowe dane w DataFrame
# data = {
#     'take_profit': [10, 20, 30, 15, 25],
#     'stop_loss': [5, 10, 15, 8, 12],
#     'balance': [1000, 1500, 1200, 1300, 1400]
# }
file_path = r'C:\Users\sebas\PycharmProjects\PythonObiektowy\wyniki_kombinacji_tp_sl.csv'
#  read data from csv file and import it into dataframe
df = pd.read_csv(file_path, sep=',', header=0)


# df = pd.DataFrame(df)

# Tworzymy macierz danych do mapy ciepła
heatmap_data = df.pivot_table(index='stop_loss', columns='take_profit', values='balance')

# Ustawienie stylu tła na ciemny
sns.set_style("darkgrid")

# Tworzymy mapę ciepła
plt.figure(figsize=(8, 6))
sns.heatmap(heatmap_data, annot=True, cmap='Blues', linewidths=0.5, fmt='.2f', vmin=-20000, vmax=10000)

# Dodajemy tytuł i etykiety osi
plt.title("Mapa ciepła: Balance w zależności od Take Profit i Stop Loss")
plt.xlabel("Take Profit")
plt.ylabel("Stop Loss")

# Wyświetlamy wykres
plt.show()
