# TweeNspector

## Authors

1. Damian Bisewski
2. Marian Buzak

## Functionalities

- Analysis of contents published by a given Twitter user
- Analysis of a given Twitter user's interactions with other users
- Statistics about a given Twitter user
![DiagramPrzypadkowUzycia](https://user-images.githubusercontent.com/92164738/169618517-1dd4697e-e496-41b4-8a51-bf8420d98e87.png)

Use case diagram of the application

## Research topics

- Analysis of vocabulary used by Twitter users (as Twitter is one of the most popular social media) 
- Analysis of interconnections between users (are there more closed bubbles or the circulation of thoughts and ideas is broader)
- Analysis of the user's behavior (frequency of writing or the number of reactions)

## Authors by responsibilities

| Responsibility | Person          |  
|:--------------:|:---------------:|
| Data analysis  | Damian Bisewski |
| Frontend       | Marian Buzak    |
| Web-scraping   | Damian Bisewski |

## Technologies

Python:

1. Web scraping - twint
2. UI - tkinter
3. Wordcloud creation - wordcloud
4. Text lemmatization - spacy
5. Additionally pandas, matplotlib.pyplot

## Input
1. Twitter username field, searched word and time frames of searched tweets
2. Functionality choice field
3. Pressing a button starts running the app and displays the result
4. Additional buttons enable the user to save the results as a file and to save the found tweets as a CSV file

## Output
For each functionality the app displays:
- **Most frequently used words**: WordCloud with most frequently used words (except the stopwords saved in stopwords.txt)

![Pekao_analizy_wordcloud](https://user-images.githubusercontent.com/92164738/169615944-b263920c-1677-49e2-b4d4-16e7c7998946.png)
WordCloud generated for the account Pekao_Analizy

- **Interconnections network of the user**: Twitter interconnections network for a user displayed as a graph

![twitteranalyser2](https://user-images.githubusercontent.com/92164738/169613771-76b2a7ba-2125-4477-838c-2d1e88f07852.png) 
Interconnections network generated for Elon Musk

- **Statistics about the user**: Graphs presenting the maximum, average and median of a given user's tweets' likes and retweets, the number of tweets created grouped by the hour of creation and the most frequently used hashtags
![POTUSgodziny](https://user-images.githubusercontent.com/92164738/169615080-458a5682-bf4a-4fd2-b661-81d6811a6986.png)
Hours (UTC+1) during which POTUS sent the last 100 tweets

![POTUSpopularnosc](https://user-images.githubusercontent.com/92164738/169615304-47d6187a-8907-4d81-82d6-84fd6d4957b9.png)
The maximum and average popularity of POTUS's last 100 tweets

## Processing workflow
The app enables conducting experiments for tweets written in Polish and English
1. The app is started and requests from the user to give:
    - searched Twitter account's username
    - time frames of searched tweets
    - the chosen functionality
2. In case of no existing account with a given username the app should display an error message
3. All results given by the app should have the possibility to be saved as PNG or CSV files. In order to save the results, the user should press a dedicated button.

## Running
1. In order to get the source code of the application you need to write in Linux Terminal or Windows Command Line:
```bash
git clone https://github.com/DamianBisewski/tweenspector
```

2. To install all libraries needed to run TweeNspector, after downloading the source file you need to write in Linux Terminal or Windows Command Line:
```bash
pip install -r requirements.txt
```
or
```bash
pip3 install -r requirements.txt
```
3. If you run the app in Linux operating system, after installing the requirements you should write in Linux Terminal:
```bash
pip install python-tk
```
or
```bash
pip3 install python-tk
```
4. To run the application, in Windows Command Line or Linux Terminal in the app folder you need to write:
```bash
python MainApplication.py
```
lub
```bash
python3 MainApplication.py
```
