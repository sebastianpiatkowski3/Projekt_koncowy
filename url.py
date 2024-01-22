import requests


def get_url(tabela):
    url = "https://api.nbp.pl/api/exchangerates/tables/" + str(tabela)
    tablea = []
    tablea_dict = {}

    # Wysyłanie zapytania GET do API
    response = requests.get(url)

    # Sprawdzenie, czy zapytanie zakończyło się sukcesem (kod odpowiedzi 200)
    if response.status_code == 200:
        # Pobranie danych w formie słownika JSON
        data = response.json()

        # Przetwarzanie danych
        for exchange_rate_table in data:
            table = exchange_rate_table['table']
            number = exchange_rate_table['no']
            effective_date = exchange_rate_table['effectiveDate']

            # print(f"Tabela: {table}")
            # print(f"Numer: {number}")
            # print(f"Data obowiązywania: {effective_date}\n")

            tablea.append(f"Tabela: {table}")
            tablea.append(f"Numer: {number}")
            tablea.append(f"Data obowiązywania: {effective_date}\n")

            # Przetwarzanie kursów walut
            for rate in exchange_rate_table['rates']:
                currency = rate['currency']
                code = rate['code']
                mid = rate['mid']

                # print(f"{currency} ({code}): {mid}")
                tablea.append(f"{currency} ({code}): {mid}")
                tablea_dict[code]=mid
            # print("\n" + "-"*40 + "\n")
            return tablea, tablea_dict
    else:
        # Wyświetlenie komunikatu w przypadku nieudanego zapytania
        print(f"Błąd: {response.status_code}")

def get_exchange():
    table_a_list, table_dict = get_url('A')
    table_b_list, table_b_dict = get_url('B')
    table_dict.update(table_b_dict)
    table_list = table_a_list + table_b_list
    return table_list, table_dict