Narzędzie do organizacji turniejów szachowych. W obecnej postaci pozwala na wprowadzanie i edycję danych graczy, turniejów, przydzielanie graczy do turniejów, generowanie par do gry zgodnie z systemem pucharowym.

# Uruchomienie:

Narzędzie do działania wymaga podania w konfiguracji bazy danych PostgreSQL, w której bedą zapisywane dane wprowadzane przez użytkownika.
Najlepiej, aby za pierwszym uruchomieniem była pusta. Plik konfiguracyjny ma nazwę `database.ini`, znajduje się w katalogu z plikiem `main.py` i ma postać:
```
[postgresql]
host=localhost
database=chess-tournament
user=chess_user
password=password
```
