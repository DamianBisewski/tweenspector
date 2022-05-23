import time

# fonts
title_font = ("Segoe UI Semibold", 20)
large_font = ('Segoe UI Semibold', 13)
small_font = ('Segoe UI', 11)
step_font = ('Segoe UI Semibold', 15)

# colors
bg = '#313131'  # background color

# count combobox
tweets_count_list = []
for i in range(100, 1001, 100):
    tweets_count_list.append(i)

# features
features = {"Nie wybrano": "UWAGA: wybierz funkcjonalność",
            "Najczęstsze słowa": "Zbiór najczęściej używanych słów dla danego użytkownika" + '\n' + "Twittera",
            "Powiązane konta": "Graf powiązanych kont z danym użytkownikiem Twittera",
            "Statystyki użytkownika": ""}


# timezone convert to string
def timezone_to_string():
    times = {0: "00", 2.5: "15", 5: "30", 7.5: "45"}
    user_time = -time.timezone / 3600
    time_str = ""
    if int(user_time) < 10:
        time_str += "0"
    time_str += str(int(user_time)) + ":"
    time_str += times[((user_time * 10) % 10)]
    return time_str
