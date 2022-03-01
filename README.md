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

## Instalacja spacy
Do lematyzacji tekstu używany jest moduł spacy, aby zainstalować odpowiedni model języka do lematyzacji, należy w wierszu polecenia wpisać 
1. !pip install spacy
2. python -m spacy download pl_core_news_lg

## Instalacja twint
Git:
git clone https://github.com/twintproject/twint.git
cd twint
pip3 install . -r requirements.txt
Pip:
pip3 install twint
or
pip3 install --user --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint

