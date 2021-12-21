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

1. web scrapping - twint. Alternatywa to tweepy (Twitter API), jednak ma bardzo istotną wadę - potrzeba tam posiadać konto na Twitterze, a także pakiet kluczy dostępu, a oprócz tego nie można obejrzeć kont, które ograniczyły widzialność swoich tweetów.
2. UI - tkinter
3. Rysowanie mapy słów - wordcloud
4. Lematyzacja tekstu - Morfeusz2, spacy (ważne - lematyzacja tekstu nie działa z dokładnością 100%!)
5. Dodatkowo pandas, matplotlib.pyplot

## Input
1. Pole wejścia na nazwę użytkownika Twittera oraz ramy czasowe tweetów (przy czym powinna istnieć możliwość wczytania tweetów bezpośrednio z Twittera albo z pliku CSV)
2. Pole wyboru w celu określenia funkcjonalności (powinno się odblokować dopiero po załadowaniu tweetów)
3. Przycisk do wyświetlenia wyników
4. Przyciski do zapisu danych w formacie .csv oraz jako obraz w formacie .png

## Output
Dla określonej funkcjonalności aplikacja wyświetla:
- **Najczęściej występujące słowa**: WordCloud z tymi słowami (oprócz słów nieznaczących - stopwords.txt)
- **Sieć powiązań użytkowników z danym kontem**: sieć powiązań użytwników Twiterra w formie grafu
- **Znalezienie kont o podobnej tematyce**: listę kont podobnych. Konto podobne oznacza w tym przypadku, że lista najczęściej występujących słów będzie zbliżona do konta wejściowego.

## Processing workflow
Aplikacja umożliwia przeprowadzenie eksperymentów dla języka polsiego i angielskiego
1. Aplikacja zostaje otwarta i prosi użytkownika o podanie:
    - nazwy uzytkownika na Twitterze
    - ram czasowych tweetów
2. Po wczytaniu nazwy użytkownika oraz ram czasowych tweetów powinna pojawić się lista tweetów oraz przycisk wyboru funkcjonalności.
3. W razie nieistnienia konta o zadanej nazwie, aplikacja powinna zwrócić komunikat o błędzie.
4. Jeśli konto istnieje, to obraz z wynikami powinien pojawić się w nowym oknie.
5. Wszystkie wyniki zwrócone przez aplikację powinny mieć możliwość zapisu do pliku CSV lub PNG. Aby tak się stało, należy wybrać odpowiedni przycisk zapisujący dane.
