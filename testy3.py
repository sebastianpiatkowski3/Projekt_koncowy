"""
This script generates all possible combinations of 0 and 1 of length 7
and saves them to a csv file.
"""

# Importujemy moduł itertools, który zawiera funkcję combinations
import itertools

# Tworzymy listę z elementami 0 i 1
lista = [0, 1]

# Używamy funkcji combinations, aby uzyskać wszystkie kombinacje o długości 7 z listy
# Konwertujemy wynik na listę i wyświetlamy go
kombinacje = list(itertools.product(lista , repeat=7))

print(kombinacje)

# save kombinacje to csv file
import csv
with open('kombinacje7.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(kombinacje)