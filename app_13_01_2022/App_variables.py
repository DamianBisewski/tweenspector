# fonts
title_font = ("Segoe UI Semibold", 20)
large_font = ('Segoe UI Semibold', 13)
small_font = ('Segoe UI', 11)
step_font = ('Segoe UI Semibold', 15)

# colors
bg = '#313131'  # background color

# count combobox
tweets_count_list = []
for i in range(100, 3001, 100):
    tweets_count_list.append(i)

# features
features = {"": "UWAGA: wybierz funkcjonalność",
            "Najczęstsze słowa": "Zbiór najczęściej używanych słów dla danego użytkownika" + '\n' + "Twittera",
            "Powiązane konta": "Graf powiązanych kont z danym użytkownikiem Twittera",
            "Statystyki użytkownika": ""}
