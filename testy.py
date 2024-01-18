klucz = "C:/users/sebas/klucz.txt"  # Plik z kluczem API

with open(klucz) as zawartosc_pliku:
    apikey = zawartosc_pliku.read().strip()  # Usunięcie ewentualnych białych znaków na początku i końcu
if apikey:
    print(apikey)
    # client = freecurrencyapi.Client(apikey)
else:
    wczytywanie = False
    flash(f"Błąd: Plik \"{klucz}\" jest pusty lub nie zawiera prawidłowego klucza.")
