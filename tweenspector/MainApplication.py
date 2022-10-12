# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as img
from tkcalendar import DateEntry
from datetime import datetime
from PIL import ImageTk, Image
import datetime
from datetime import date
from App_variables import *
from FeatureStrategy import UserWordConnection, RelatedPeopleConnection, AccountsInfo
from TweetsData import TweetsData, save_tweets_df_to_csv
from sys import platform


def remove_widgets(*item_list):
    for item in item_list:
        if type(item) is list:
            for i in item:
                i.destroy()
        else:
            if item is not None:
                item.destroy()


class MainApplication:
    def __init__(self, parent):
        self.parent = parent
        self.parent.configure(background=bg)
        self.parent.geometry('700x750')
        self.parent.title('TweeNspector')
        if platform == "win32":
            self.parent.wm_iconbitmap('images/app_icon.ico')
        self.parent.resizable(True, True)

        self.main_f = None  # frames
        self.nav_b = []  # buttons
        self.save_b = None
        self.csv_save_b = None
        self.title_l = None  # labels
        self.nav_l = []
        self.step_l = []
        self.act_l = None
        self.error_l = []
        self.nav_e = []  # entries
        self.date_e = []  # date entry
        self.nav_cb = []  # combo boxes
        self.stats_rb = []  # radio buttons
        self.stats_option = 0
        self.community_detection_method_cb = []
        self.community_detection_method_l = []
        self.community_detection_method = []
        self.feature_strategy = None

        self.user_name, self.search_words, self.date_from, self.date_to, self.tweets_count = \
            None, None, None, None, None

        # start page
        self.start_page()

    def start_page(self):
        self.main_f = tk.Frame(self.parent, bg=bg)
        self.main_f.grid(row=1, column=1)

        self.title_l = tk.Label(self.main_f, text="TweeNspector", font=title_font, bg=bg, fg="white")

        self.nav_l = [tk.Label(self.main_f, text="Nazwa użytkownika", fg="white", bg=bg, font=large_font),
                      tk.Label(self.main_f, text="Poszukiwane słowo", fg="white", bg=bg, font=large_font),
                      tk.Label(self.main_f, text="Liczba tweetów", fg="white", bg=bg, font=large_font),
                      tk.Label(self.main_f, text="Data początkowa", fg="white", bg=bg, font=large_font),
                      tk.Label(self.main_f, text="Data końcowa", fg="white", bg=bg, font=large_font),
                      tk.Label(self.main_f, text="Wybierz funkcjonalność", fg="white", bg=bg, font=large_font)]

        self.step_l = [
            tk.Label(self.main_f, text="Krok 1: Podaj nazwę użytkownika i/lub poszukiwane słowo", fg="white", bg=bg,
                     font=step_font),
            tk.Label(self.main_f, text="Krok 2: Ustal liczbę tweetów i określ ramy czasowe",
                     fg="white", bg=bg, font=step_font),
            tk.Label(self.main_f, text="Krok 3: Wybierz funkcjonalność", fg="white", bg=bg, font=step_font)]

        self.nav_e = [tk.Entry(self.main_f, width=25, font=small_font, bd=2),
                      tk.Entry(self.main_f, width=25, font=small_font, bd=2)]

        default = date.today() - datetime.timedelta(days=30)
        defday = default.day
        defmon = default.month
        defyear = default.year
        self.date_e = [DateEntry(self.main_f, selectmode="day", font=small_font, date_pattern="dd.mm.yyyy", day=defday,
                                 month=defmon, year=defyear),
                       DateEntry(self.main_f, selectmode="day", font=small_font, date_pattern="dd.mm.yyyy")]

        self.nav_cb = [ttk.Combobox(self.main_f, font=small_font),
                       ttk.Combobox(self.main_f, font=small_font, width=10),
                       ]

        self.date_e[0]["state"] = "readonly"
        self.date_e[1]["state"] = "readonly"

        self.nav_cb[0]["values"] = list(features.keys())
        self.nav_cb[0].current(0)
        self.nav_cb[0]["state"] = "readonly"  # block user update combobox
        self.nav_cb[0].bind("<<ComboboxSelected>>", self.set_combobox_description)

        self.nav_cb[1]["values"] = tweets_count_list
        self.nav_cb[1].current(0)
        self.nav_cb[1]["state"] = "readonly"  # block user update combobox

        self.nav_b = [tk.Button(self.main_f, command=lambda: self.search_result(self.nav_cb[0].get()),
                                highlightthickness=0, bd=0),
                      tk.Button(self.main_f, text="zapis do csv",
                                command=lambda: self.save_csv(),
                                highlightthickness=0, bd=0)]
        path = "images/search_button.png"
        self.img = ImageTk.PhotoImage(Image.open(path))
        self.nav_b[0].config(image=self.img)

        self.img2 = ImageTk.PhotoImage(Image.open("images/save_csv.png"))
        self.nav_b[1].config(image=self.img2)

        # grid
        self.title_l.grid(row=1, column=1, padx=(40, 0), pady=(40, 20), sticky="wn")

        left_margin, step_margin = 100, 75

        self.step_l[0].grid(row=2, column=1, columnspan=2, pady=(10, 0), padx=(step_margin, 0), sticky="nw")
        self.nav_l[0].grid(row=3, column=1, pady=(10, 0), padx=(left_margin, 0), sticky="nw")
        self.nav_e[0].grid(row=3, column=2, pady=(10, 0), padx=(20, 0), sticky="nw")
        self.nav_l[1].grid(row=4, column=1, pady=(10, 0), padx=(left_margin, 0), sticky="nw")
        self.nav_e[1].grid(row=4, column=2, pady=(10, 0), padx=(20, 0), sticky="nw")

        self.step_l[1].grid(row=6, column=1, columnspan=2, pady=(10, 0), padx=(step_margin, 0), sticky="nw")
        self.nav_l[2].grid(row=7, column=1, pady=(10, 0), padx=(left_margin, 0), sticky="nw")
        self.nav_cb[1].grid(row=7, column=2, pady=(10, 0), padx=(20, 0), sticky="nw")
        self.nav_l[3].grid(row=8, column=1, pady=(10, 0), padx=(left_margin, 0), sticky="nw")
        self.date_e[0].grid(row=8, column=2, pady=(10, 0), padx=(20, 0), sticky="nw")
        self.nav_l[4].grid(row=9, column=1, pady=(10, 0), padx=(left_margin, 0), sticky="nw")
        self.date_e[1].grid(row=9, column=2, pady=(10, 0), padx=(20, 0), sticky="nw")

        self.step_l[2].grid(row=10, column=1, columnspan=2, pady=(10, 0), padx=(step_margin, 0), sticky="nw")
        self.nav_l[5].grid(row=11, column=1, pady=(10, 0), padx=(left_margin, 0), sticky="nw")
        self.nav_cb[0].grid(row=11, column=2, pady=(10, 0), padx=(20, 0), sticky="nw")

        self.nav_b[0].grid(row=15, column=1, pady=(50, 0), padx=(step_margin, 0), sticky="ne")
        self.nav_b[1].grid(row=15, column=2, pady=(50, 0), padx=(step_margin, 0), sticky="nw")

    # parameter "event" is required
    def set_combobox_description(self, event):
        # remove widgets
        remove_widgets(self.stats_rb)  # self.igraph_lb
        remove_widgets(self.community_detection_method_cb)
        remove_widgets(self.community_detection_method_l)

        # set description
        remove_widgets(self.act_l)
        picked_feature = self.nav_cb[0].get()
        self.act_l = tk.Label(self.main_f, text=features[picked_feature],
                              bg=bg, fg="white", font=small_font)
        self.act_l.grid(row=13, column=1, columnspan=2, padx=(100, 0), sticky="nw")

        def set_interconnections_network_option():
            def callback_community_detection_method(event):
                self.community_detection_method = event.widget.get()

            self.community_detection_method_cb = ttk.Combobox(self.main_f, font=small_font)
            self.community_detection_method_cb["values"] = ("Optimal Modularity", "Spinglass",
                                                            "Label Propagation", "Infomap")
            self.community_detection_method_cb.current(0)
            self.community_detection_method_cb.grid(column=2, row=14, pady=(10, 0),
                                                    padx=(20, 0), sticky="nw")
            self.community_detection_method_cb["state"] = "readonly"
            self.community_detection_method_cb.bind("<<ComboboxSelected>>",
                                                    callback_community_detection_method)
            self.community_detection_method_l = ttk.Label(self.main_f, text="Metoda grupowania kont",
                                                          foreground="white", background=bg)
            self.community_detection_method_l.grid(column=1, row=14, pady=(10, 0),
                                                   padx=(100, 0), sticky="nw")
            self.community_detection_method = self.community_detection_method_cb.get()

        def set_user_statistics_option():
            def set_radio_value():
                self.stats_option = var.get()

            var = tk.IntVar()
            self.stats_rb = [tk.Radiobutton(self.main_f, text="Reakcje na tweety", value=1),
                             tk.Radiobutton(self.main_f, text="Godzina publikacji", value=2),
                             tk.Radiobutton(self.main_f, text="Hasztagi", value=3)]

            var.set(1)  # default value 1 - "reakcje na tweety"

            for rb in self.stats_rb:
                rb.configure(selectcolor=bg, activebackground=bg, activeforeground="white", bg=bg, fg="white",
                             command=lambda: set_radio_value(), font=small_font, variable=var)

            for i in range(len(self.stats_rb)):
                self.stats_rb[i].grid(row=i + 12, column=1, padx=(100, 0), pady=(10, 0), sticky="nw")
            self.stats_option = var.get()

        if picked_feature == "Powiązane konta":
            set_interconnections_network_option()
        elif picked_feature == "Statystyki użytkownika":
            set_user_statistics_option()

    def propagate_params(self):
        user_name = self.nav_e[0].get()
        search_words = self.nav_e[1].get()
        tweets_count = self.nav_cb[1].get()
        if user_name == '':
            user_name = None
        if search_words == '':
            search_words = None
        if user_name is None:
            tk.messagebox.showerror("Błąd", "Proszę podać nazwę użytkownika/poszukiwane słowo")
            return False
        format1 = self.date_e[0].get().split(".")[::-1]
        date_from = format1[0] + "-" + format1[1] + "-" + format1[2]

        format2 = self.date_e[1].get().split(".")[::-1]
        date_to = format2[0] + "-" + format2[1] + "-" + format2[2]
        if date_from >= date_to:
            tk.messagebox.showerror("Błąd", "Data początkowa późniejsza od daty końcowej")
            return False

        self.user_name = user_name
        self.search_words = search_words
        self.date_from = date_from
        self.date_to = date_to
        self.tweets_count = tweets_count

        # remove errors
        remove_widgets(self.error_l)
        return True

    def search_result(self, feature):
        if not self.propagate_params():
            return
        if feature == "Nie wybrano":
            tk.messagebox.showerror("Błąd", "Proszę wybrać jedną z funkcjonalności")
            return
        self.configure_feature_strategy(feature, self.user_name, self.search_words, self.date_from,
                                        self.date_to, self.tweets_count,
                                        self.stats_option, self.community_detection_method)

        if not self.feature_strategy.generate_image():
            tk.messagebox.showerror("Błąd", "Podany użytkownik nie istnieje, został zablokowany lub nie "
                                            "opublikował "
                                            "żadnych tweetów spełniających warunki wyszukiwania")
        else:
            image = img.imread("images/file.png")
            matplotlib.use("TkAgg")
            plt.figure(figsize=(12, 5))
            plt.axis("off"), plt.imshow(image)
            plt.tight_layout()
            plt.show(block=False)  # helps with terminate program

    def configure_feature_strategy(self, feature, user_name, search_words, date_from, date_to, tweets_count,
                                   stats_option,
                                   community_detection_method):
        if feature == "Najczęstsze słowa":
            self.feature_strategy = UserWordConnection(user_name, search_words, date_from, date_to, tweets_count)
        elif feature == "Powiązane konta":
            self.feature_strategy = RelatedPeopleConnection(user_name, search_words, date_from, date_to,
                                                            tweets_count, community_detection_method)
        elif feature == "Statystyki użytkownika":
            self.feature_strategy = AccountsInfo(user_name, search_words, date_from, date_to, tweets_count,
                                                 stats_option)
        return True

    def save_csv(self):
        if not self.propagate_params():
            return
        td = TweetsData(self.user_name, self.search_words, self.date_from, self.date_to, self.tweets_count)
        df = td.get_tweets(self.user_name, self.search_words, self.date_from, self.date_to, self.tweets_count)
        data = [('All types(*.*)', '*.*'),
                ('csv file(*.csv)', '*.csv')]
        file = asksaveasfile(filetypes=data, defaultextension=data)
        if file:
            save_tweets_df_to_csv(file.name, df)


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()
