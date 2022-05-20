# Projekt zespołowy

## Osoby

1. Damian Bisewski
2. Marian Buzak

## Funkcjonalności

- analiza treści postów danego użytkownika
- analiza interakcji danego użytkownika z innymi użytkownikami
- statystyki o użytkowniku

## Aspekt badawczy

- analiza słownictwa używanego przez użytkowników Twittera (jednego z najpopularniejszych portali społecznościowych)
- analiza powiązań między użytkownikami Twittera (czy mamy do czynienia z hermetycznymi bańkami czy wymiana myśli jest szersza)
- analiza zachowań użytkownika (częstotliwości pisania czy liczby generowanych reakcji)

## Podział

| Podział        | Osoba           |  
|:--------------:|:---------------:|
| analiza danych | Damian Bisewski |
| frontend       | Marian Buzak    |
| web-scrapping  | Damian Bisewski |

## Technologie

Python:

1. web scraping - twint
2. UI - tkinter
3. Rysowanie mapy słów - wordcloud
4. Lematyzacja tekstu - Morfeusz2, spacy
5. Dodatkowo pandas, matplotlib.pyplot

## Input
1. Pole wejścia na nazwę użytkownika Twittera oraz ramy czasowe tweetów
2. Pole wyboru w celu określenia funkcjonalności
3. Przycisk do wyświetlenia wyników
4. Przyciski do zapisu danych w formacie .csv oraz jako obraz w formacie .png

## Output
Dla określonej funkcjonalności aplikacja wyświetla:
- **Najczęściej występujące słowa**: WordCloud z tymi słowami (oprócz słów nieznaczących - stopwords.txt)
- **Sieć powiązań użytkowników z danym kontem**: sieć powiązań użytwników Twittera w formie grafu
- **Statystyki o użytkowniku**: Wykresy prezentujące najwyższą, najniższą i średnią liczbę polubień oraz podań dalej tweetów użytkownika, lokalizacje, z których pisał użytkownik, konta, którym najczęściej odpisywał użytkownik, godziny, w których najczęściej pisał użytkownik oraz hasztagi, jakich używał użytkownik

## Processing workflow
Aplikacja umożliwia przeprowadzenie eksperymentów dla języka polskiego i angielskiego
1. Aplikacja zostaje otwarta i prosi użytkownika o podanie:
    - nazwy uzytkownika na Twitterze
    - ram czasowych tweetów
    - wybranej funkcjonalności
2. W razie nieistnienia konta o zadanej nazwie, aplikacja powinna zwrócić komunikat o błędzie
3. Wszystkie wyniki zwrócone przez aplikację powinny mieć możliwość zapisu do pliku CSV lub PNG. Aby tak się stało, należy wybrać odpowiedni przycisk zapisujący dane

## Uruchomienie
1. Aby zainstalować wszystkie biblioteki, z których składa się urządzenie, po ściągnięciu źródeł należy wpisać komendę:
pip install requirements.txt
3. Aby uruchomić aplikację, należy wpisać w katalogu app komendę:
python MainApplication.py

## Aplikacja w akcji
![twitteranalyser2](https://user-images.githubusercontent.com/92164738/169613771-76b2a7ba-2125-4477-838c-2d1e88f07852.png) 
Przykładowa sieć powiązań wygenerowana dla Elona Muska

![POTUSgodziny](https://user-images.githubusercontent.com/92164738/169615080-458a5682-bf4a-4fd2-b661-81d6811a6986.png)
Godziny, w których konto POTUS wysłało ostatnie 100 tweetów (wg strefy czasowej UTC+1)

![POTUSpopularnosc](https://user-images.githubusercontent.com/92164738/169615304-47d6187a-8907-4d81-82d6-84fd6d4957b9.png)
Maksymalna i średnia popularność ostatnich 100 tweetów konta POTUS

![Pekao_analizy_wordcloud](https://user-images.githubusercontent.com/92164738/169615944-b263920c-1677-49e2-b4d4-16e7c7998946.png)
Mapa słów wygenerowana dla konta Pekao_Analizy

![DiagramPrzypadkowUzycia](https://user-images.githubusercontent.com/92164738/169618517-1dd4697e-e496-41b4-8a51-bf8420d98e87.png)
Diagram przypadków użycia aplikacji
