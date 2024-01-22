class Reader:
    """
    Klasa Reader służy do wczytywania danych z plików.

    Atrybuty:
        file_klucz (str): Ścieżka do pliku z kluczem API.
        file_symbols (str): Ścieżka do pliku z symbolami.
        symbols_list (list): Lista wczytanych symboli.

    Metody:
        __init__(): Inicjalizuje obiekt klasy Reader.

        load_key(): Wczytuje klucz API z pliku.

        load_symbols(): Wczytuje symbole z pliku.

    Przykład użycia:
        reader = Reader()
        api_key, error_key = reader.load_key()
        symbols_list, error_symbols = reader.load_symbols()
    """

    def __init__(self):
        """
        Inicjalizuje obiekt klasy Reader.

        Atrybuty:
            file_klucz (str): Ścieżka do pliku z kluczem API.
            file_symbols (str): Ścieżka do pliku z symbolami.
            symbols_list (list): Lista wczytanych symboli.
        """
        self.file_klucz = "C:/users/sebas/klucz.txt"  # Plik z kluczem API
        self.file_symbols = "waluty.txt"
        self.symbols_list = []

    def load_key(self):
        """
        Wczytuje klucz API z pliku.

        Zwraca:
            tuple: Krotka zawierająca klucz API i informację o błędzie. (None, error) w przypadku błędu.

        Przykład użycia:
            api_key, error = reader.load_key()
        """
        try:
            with open(self.file_klucz) as zawartosc_pliku:
                apikey = zawartosc_pliku.read().strip()
        except FileNotFoundError as e:
            return None, f"Błąd: Plik \"{self.file_klucz}\" nie istnieje. {e}"

        if apikey:
            return apikey, None
        else:
            return None, f"Błąd: Plik \"{self.file_klucz}\" jest pusty lub nie zawiera prawidłowego klucza."

    def load_symbols(self):
        """
        Wczytuje symbole z pliku.

        Zwraca:
            tuple: Krotka zawierająca listę symboli i informację o błędzie. (None, error) w przypadku błędu.

        Przykład użycia:
            symbols_list, error = reader.load_symbols()
        """
        try:
            with open(self.file_symbols, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError as e:
            return None, f"Błąd: Plik \"{self.file_symbols}\" nie istnieje. {e}"

        if lines:
            self.symbols_list = [line.strip() for line in lines]
            return self.symbols_list, None
        else:
            return None, f"Błąd: Plik \"{self.file_symbols}\" jest pusty."
