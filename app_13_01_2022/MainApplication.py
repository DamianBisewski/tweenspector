import tkinter as tk
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as img
from App_variables import *
from FeatureStrategy import FeatureStrategy
from tkcalendar import DateEntry


class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.configure(background=bg)
        self.parent.geometry('600x700')
        self.parent.title('TwitterData')
        #self.parent.resizable(False, False)

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
        self.igraph_lb = None  # list boxes
        self.stats_option = 0
        self.feature_strategy = None

        # start page
        self.StartPage()

    def StartPage(self):
        self.main_f = tk.Frame(self.parent, bg=bg)
        self.main_f.grid(row=1, column=1)

        self.title_l = tk.Label(self.main_f, text="TwitterData", font=title_font, bg=bg, fg="white")

        self.nav_l = [tk.Label(self.main_f, text="Nazwa użytkownika", fg="white", bg=bg, font=large_font),
                      tk.Label(self.main_f, text="Liczba twettów", fg="white", bg=bg, font=large_font),
                      tk.Label(self.main_f, text="Data początkowa", fg="white", bg=bg, font=large_font),
                      tk.Label(self.main_f, text="Data końcowa", fg="white", bg=bg, font=large_font),
                      tk.Label(self.main_f, text="Wybierz funkcjonalność", fg="white", bg=bg, font=large_font)]

        self.step_l = [tk.Label(self.main_f, text="Krok 1: Podaj nazwę użytkownika", fg="white", bg=bg, font=step_font),
                       tk.Label(self.main_f, text="Krok 2: Ustal liczbę tweetów i określ ramy czasowe",
                                fg="white", bg=bg, font=step_font),
                       tk.Label(self.main_f, text="Krok 3: Wybierz funkcjonalność", fg="white", bg=bg, font=step_font)]

        self.nav_e = [tk.Entry(self.main_f, width=25, font=small_font)]

        self.date_e = [DateEntry(self.main_f, selectmode="day", font=small_font, date_pattern="dd.mm.yyyy"),
                       DateEntry(self.main_f, selectmode="day", font=small_font, date_pattern="dd.mm.yyyy")]

        self.nav_cb = [ttk.Combobox(self.main_f, font=small_font),
                       ttk.Combobox(self.main_f, font=small_font, width=10)]

        self.date_e[0]["state"] = "readonly"
        self.date_e[1]["state"] = "readonly"

        self.nav_cb[0]["values"] = list(features.keys())
        self.nav_cb[0]["state"] = "readonly"  # block user update combobox
        self.nav_cb[0].bind("<<ComboboxSelected>>", self.set_combobox_description)

        self.nav_cb[1]["values"] = tweets_count_list
        self.nav_cb[1]["state"] = "readonly"  # block user update combobox

        self.nav_b = tk.Button(self.main_f, text="Wyszukaj", command=lambda: self.search_result(self.nav_cb[0].get()))

        # grid
        self.title_l.grid(row=1, column=1, padx=(40, 0), pady=(40, 20), sticky="wn")

        left_margin, step_margin = 100, 75

        self.step_l[0].grid(row=2, column=1, columnspan=2, pady=(10, 0), padx=(step_margin, 0), sticky="nw")
        self.nav_l[0].grid(row=3, column=1, pady=(10, 0), padx=(left_margin, 0), sticky="nw")
        self.nav_e[0].grid(row=3, column=2, pady=(10, 0), padx=(20, 0), sticky="nw")

        self.step_l[1].grid(row=5, column=1, columnspan=2, pady=(10, 0), padx=(step_margin, 0), sticky="nw")
        self.nav_l[1].grid(row=6, column=1, pady=(10, 0), padx=(left_margin, 0), sticky="nw")
        self.nav_cb[1].grid(row=6, column=2, pady=(10, 0), padx=(20, 0), sticky="nw")
        self.nav_l[2].grid(row=7, column=1, pady=(10, 0), padx=(left_margin, 0), sticky="nw")
        self.date_e[0].grid(row=7, column=2, pady=(10, 0), padx=(20, 0), sticky="nw")
        self.nav_l[3].grid(row=8, column=1, pady=(10, 0), padx=(left_margin, 0), sticky="nw")
        self.date_e[1].grid(row=8, column=2, pady=(10, 0), padx=(20, 0), sticky="nw")

        self.step_l[2].grid(row=9, column=1, columnspan=2, pady=(10, 0), padx=(step_margin, 0), sticky="nw")
        self.nav_l[4].grid(row=10, column=1, pady=(10, 0), padx=(left_margin, 0), sticky="nw")
        self.nav_cb[0].grid(row=10, column=2, pady=(10, 0), padx=(20, 0), sticky="nw")

        self.nav_b.grid(row=15, column=1, pady=(10, 0), padx=(step_margin, 0), sticky="nw")

    # parameter "event" is required
    def set_combobox_description(self, event):
        # remove widgets
        self.remove_widgets(self.stats_rb, self.igraph_lb)

        # set description
        self.remove_widgets(self.act_l)
        picked_feature = self.nav_cb[0].get()
        self.act_l = tk.Label(self.main_f, text=features[picked_feature],
                              bg=bg, fg="white", font=small_font)
        self.act_l.grid(row=11, column=1, columnspan=2, padx=(100, 0), sticky="nw")

        def set_user_statistics_option():
            def set_radio_value():
                self.stats_option = var.get()

            var = tk.IntVar()
            self.stats_rb = [tk.Radiobutton(self.main_f, text="Reakcje na tweety", value=1),
                             tk.Radiobutton(self.main_f, text="Godzina publikacji", value=2),
                             tk.Radiobutton(self.main_f, text="Hasztagi", value=3)]

            for rb in self.stats_rb:
                rb.configure(selectcolor=bg, activebackground=bg, activeforeground="white", bg=bg, fg="white",
                             command=lambda: set_radio_value(), font=small_font,  variable=var)

            for i in range(len(self.stats_rb)):
                self.stats_rb[i].grid(row=i+12, column=1, padx=(100, 0), pady=(10, 0), sticky="nw")

        def set_user_connection_option():
            self.igraph_lb = tk.Listbox(self.main_f)
            self.igraph_lb.grid(row=12, column=1, padx=(100, 0), pady=(10, 0), sticky="nw")
        if picked_feature == "Statystyki użytkownika":
            set_user_statistics_option()
        elif picked_feature == "Powiązane konta":
            set_user_connection_option()

    def search_result(self, feature):
        text_input = self.nav_e[0].get()
        tweets_count = self.nav_cb[1].get()
        date_from = ''  # self.date_e[0].get()
        date_to = ''  # self.date_e[1].get()
        search_words = ''  # TBD

        valid_graph = self.is_provide_data_valid(feature, text_input, search_words, date_from, date_to, tweets_count)

        if valid_graph:
            # remove errors
            self.remove_widgets(self.error_l)
            self.feature_strategy.feature.generate_image(self.stats_option)

            image = img.imread("file.png")
            matplotlib.use("TkAgg")
            plt.figure(figsize=(12, 5))

            plt.axis("off"), plt.imshow(image)
            plt.tight_layout()
            plt.show(block=False)  # helps with terminate program

            from TweetsData import save_tweets_df_to_csv
            #save_tweets_df_to_csv("cos.csv", )

    def is_provide_data_valid(self, feature, text_input, search_words, date_from, date_to, tweets_count):
        for entry in self.nav_e:
            if entry.get() == "":
                return False
        if feature == "":
            return False
        self.feature_strategy = FeatureStrategy(feature, text_input, search_words, date_from, date_to, tweets_count)
        date_frame = self.feature_strategy.feature.get_tweets(text_input, search_words,
                                                              date_from, date_to, tweets_count)
        if date_frame is False:
            self.error_l = [tk.Label(self.main_f, text="Taki użytkownik nie istnieje!", bg=bg, fg="red",
                                     font=small_font)]
            self.error_l[0].grid(row=4, column=1, padx=(100, 0))
            return False
        return True

    def remove_widgets(self, *item_list):
        for item in item_list:
            if type(item) is list:
                for i in item:
                    i.destroy()
            else:
                if item is not None:
                    item.destroy()

    def save_csv(self):
        pass

    def set_date_format(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()
