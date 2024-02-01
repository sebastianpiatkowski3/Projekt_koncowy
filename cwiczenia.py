lista = [i for i in range(1, 1110)]
print(lista)

if 13 in lista:
    print('jest 13 w lista')


lista_zagniezdzona = [[1, 2, 3], [4, 5, 6], [7, 8, ["a", "b"]]]
for podlista in lista_zagniezdzona:
    print(podlista)
    print(type(podlista))
    for element in podlista:
        print(element)
print('\n')
print(lista_zagniezdzona[2][1])