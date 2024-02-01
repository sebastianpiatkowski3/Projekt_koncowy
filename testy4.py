"""
This script generates all possible combinations with repetitions of 0 and 1 of length 'ile_powtorzen'
and takes the mirror image of each combination.
then save combinations without mirrors to csv file.
Mirror explanation: For example:
0,1,0,1,1,0,1 has mirror image 1,0,1,0,0,1,0
"""

# Importujemy moduł itertools, który zawiera funkcję combinations
import itertools
ile_powtorzen = 7
# Tworzymy listę z elementami 0 i 1
lista = [0, 1]

# Używamy funkcji combinations, aby uzyskać wszystkie kombinacje o długości 7 z listy
# Konwertujemy wynik na listę i wyświetlamy go
kombinacje = list(itertools.product(lista , repeat=ile_powtorzen))


# Tworzymy słownik, w którym będziemy przechowywać pary (kombinacja 0 i 1) : lustro
slownik = {}
bez_luster = {}

# Dla każdej kombinacji z listy kombinacje
for kombinacja in kombinacje:
    # Tworzymy nową kombinację, która jest lustrem kombinacji oryginalnej
    lustro = [int(not x) for x in kombinacja]
    # Dodajemy parę (kombinacja 0 i 1) : lustro do słownika
    slownik[kombinacja] = lustro


# Wyświetlamy wynik
for key, value in enumerate(slownik.items()):
    print(key, value)

print("-" * 50)
#  i need only 64 firs kesy from dictionary
print('Combinations without mirror image:')
combinations_bez_luster = int((2 ** ile_powtorzen)/2)
new_dict = dict(list(slownik.items())[0:combinations_bez_luster])
print(len(new_dict))
for key, value in enumerate(new_dict.items()):
    print(key, value)
#  create list with keys from new_dict
list_keys = []
for key, value in new_dict.items():
    list_keys.append(key)

# save kombinacje without mirrors to csv file
file_name = 'kombinacje_without_mirror' + str(ile_powtorzen) + '.csv'
import csv
with open(file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(list_keys)

# save all kombinacje to csv file
file_name = 'kombinacje' + str(ile_powtorzen) + '.csv'
import csv
with open(file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerows(kombinacje)