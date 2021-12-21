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

1. web scrapping - twint
2. UI - tkinter
3. Rysowanie mapy słów - wordcloud
4. Lematyzacja tekstu - Morfeusz2
5. Dodatkowo pandas, matplotlib.pyplot

## Input
1. Pole wejścia na nazwę użytkownika Twittera oraz ramy czasowe twettów
2. Pole wejścia wyrażone w procentach do określenia sieci powiązań danego użytkownika Twittera (z jakimi kontami dany użytkownik ma najwięcej interakcji)
3. Pole wyboru w celu określenia funkcjonalności
4. Przycisk do wyświetlenia wyników
5. Przyciski do zapisu danych w formacie .csv oraz jako obraz w formacie .png

## Output
Dla określonej funkcjonalności aplikacja wyświetla:
- **Najczęściej występujące słowa**: WordCloud z tymi słowami (oprócz słów nieznaczących - stopwords.txt)
- **Sieć powiązań użytkowników z danym kontem**: sieć powiązań użytwników Twiterra w formie grafu
- **Znalezienie kont o podobnej tematyce**: listę kont podobnych

## Processing workflow
Aplikacja umożliwia przeprowadzenie eksperymentów dla języka polsiego i angielskiego
1. Aplikacja zostaje otwarta i prosi użytkownika o podanie:
    - nazwy uzytkownika na Twitterze
    - ram czasowych twettów
    - wybranej funkcjonalności
2. W razie nieistnienia konta o zadanej nazwie, aplikacja powinna zwrócić komunikat o błędzie
3. Wszystkie wyniki zwrócone przez aplikację powinny mieć możliwość zapisu do pliku CSV lub PNG. Aby tak się stało, należy wybrać odpowiedni przycisk zapisujący dane
