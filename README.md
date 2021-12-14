# Projekt zespołowy

## Osoby

1. Damian Bisewski
2. Marian Buzak
3. Jakub Chyła

## Funkcjonalności

- analiza treści postów danego użytkownika
- rekomendacja podobnych kont na podstawie treści
- wyszukanie użytkowników najczęściej piszących na dany temat

## Aspekt badawczy

Analiza postów i treści udostępnianych przez danego użytkownika oraz znalezienie powiązań z innymi
użytkownikami na ich podstawie.

## Podział

| Podział        | Osoba           |  
|:--------------:|:---------------:|
| analiza danych | Damian Bisewski |
| frontend       | Marian Buzak    |
| web-scrapping  | Damian Bisewski |

## Technologie

Python:

1. web scrapping - BeautifulSoup
2. UI - tkinter

## Input
1. Pole wejścia na nazwę użytkownika Twittera oraz ramy czasowe twettów
2. Pole wejścia do określenia dokładności powiązań między słowami
3. Przycisk do wybrania funkcjonalności
4. Przycisk do wyświetlenia wyników

## Output
Dla określonej funkcjonalności aplikacja wyświetla:
- **Najczęściej występujące słowa**: WordCloud z tymi słowami (oprócz słów nieznaczących)
- **Sieć powiązań użytkowników z danym kontem**: sieć powiązań w formie grafu
- **Znalezienie kont o podobnej tematyce**: listę kont podobnych

## Processing workflow
1. Aplikacja zostaje otwarta i prosi użytkownika o podanie nazwy użytkownika na Twitterze oraz ram czasowych(w razie nieistnienia konta o zadanej nazwie, aplikacja powinna zwrócić komunikat o błędzie)
2. Po podaniu nazwy istniejącego konta powinna wyświetlić się lista tweetów zdobytych dzięki funkcjonalności biblioteki twint. Wtedy użytkownik powinien mieć do wyboru jedną z trzech dostępnych funkcjonalności
3. Wszystkie wyniki zwrócone przez aplikację powinny mieć możliwość zapisu do pliku CSV. Aby tak się stało, należy wprowadzić odpowiedni przycisk. Jego wciśnięcie miałoby spowodować zapis do CSV
