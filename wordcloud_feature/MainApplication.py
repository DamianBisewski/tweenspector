import os.path
import tkinter as tk
from tkinter import ttk, filedialog
from App_variables import *
from PIL import Image, ImageTk
from FeatureStrategy import FeatureStrategy


class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.configure(background=bg)
        self.parent.geometry('1350x750')
        self.parent.title('Searched phrases on Twitter')
        # self.parent.resizable(False, False)

        self.nav_f, self.act_f, self.graph_f = None, None, None  # frames
        self.nav_b, self.act_b = [], []  # buttons
        self.save_b, self.csv_save_b = None, None
        self.title_l, self.nav_l, self.act_l, self.graph_l = None, [], None, []  # labels
        self.nav_e = []  # entries
        self.nav_cb = None  # combo box
        # self.tweets_data = None
        self.feature_strategy = None
        self.canvas = None

        self.graph_position = True
        # start page
        self.StartPage()

    def StartPage(self):
        self.nav_f = tk.Frame(self.parent, bg=bg)
        self.nav_f.grid(row=1, column=1)

        self.graph_f = tk.Frame(self.parent, bg=bg)
        self.graph_f.grid(row=2, column=1, sticky="nsew")

        self.title_l = tk.Label(self.nav_f, text="App name", font=title_font, bg=bg, fg="white")

        self.nav_l = [tk.Label(self.nav_f, text="Nazwa użytkownika", fg="white", bg=bg, font=large_font)]
        self.nav_l.append(tk.Label(self.nav_f, text="Liczba twettów", fg="white", bg=bg, font=large_font))
        self.nav_l.append(tk.Label(self.nav_f, text="Wybierz funkcjonalność", fg="white", bg=bg, font=large_font))

        self.nav_e = [tk.Entry(self.nav_f, width=25, font=small_font)]
        self.nav_e.append(tk.Entry(self.nav_f, width=25, font=small_font))

        self.nav_cb = ttk.Combobox(self.nav_f, font=small_font)
        self.nav_cb["values"] = list(features.keys())
        self.nav_cb["state"] = "readonly"

        self.nav_cb.bind("<<ComboboxSelected>>", self.set_combobox_description)

        self.nav_b = tk.Button(self.nav_f, text="Wyszukaj", command=lambda: self.search_result(self.nav_cb.get()))

        # grid
        self.title_l.grid(row=1, column=1, columnspan=len(self.nav_l)+1, pady=(40, 20))

        self.nav_l[0].grid(row=2, column=1, pady=(10, 0), padx=(300, 0))
        self.nav_l[1].grid(row=2, column=2, pady=(10, 0), padx=(50, 0))
        self.nav_l[2].grid(row=2, column=3, pady=(10, 0), padx=(50, 0))
        self.nav_e[0].grid(row=3, column=1, pady=(10, 0), padx=(300, 0))
        self.nav_e[1].grid(row=3, column=2, pady=(10, 0), padx=(50, 0))

        self.nav_b.grid(row=3, column=4, pady=(10, 0), padx=(50, 300))
        self.nav_cb.grid(row=3, column=3, pady=(10, 0), padx=(50, 0))

    def set_combobox_description(self, event):
        self.remove_widgets(self.act_l)
        picked_feature = self.nav_cb.get()
        self.act_l = tk.Label(self.nav_f, text=features[picked_feature],
                              bg=bg, fg="white", font=large_font)
        self.act_l.grid(row=4, column=1, columnspan=len(self.nav_l)+1, padx=(300, 0), sticky="nw")

    def search_result(self, feature):
        text_input = self.nav_e[0].get()
        tweets_count = self.nav_e[1].get()
        valid_graph = True

        for entry in self.nav_e:
            valid_graph = self.valid_graph(entry)
        try:
            tweets_count = int(tweets_count)
        except ValueError:
            self.nav_e[1].configure(bg='red')
            valid_graph = False

        if feature == "":
            valid_graph = False
        if valid_graph:
            # IMPORTANT: remove labels!!!
            if self.graph_position is True:
                self.graph_position = False
                image_column = 1
            else:
                self.graph_position = True
                image_column = 2
            self.feature_strategy = FeatureStrategy(feature, text_input, tweets_count)
            self.feature_strategy.feature.generate_image()

            image_shape = (350, 600)

            self.graph_l = tk.Label(self.graph_f, font=large_font, bg=bg, fg="white",
                                    text=self.feature_strategy.feature.set_graph_label())
            self.graph_l.grid(row=1, column=image_column, padx=(50, 0), pady=(50, 0))

            self.canvas = tk.Canvas(self.graph_f, height=image_shape[0], width=image_shape[1])
            self.canvas.grid(row=2, column=image_column, padx=(50, 0), pady=(10, 0))

            path = 'file.png'
            image = Image.open(path)
            self.canvas.image = ImageTk.PhotoImage(image.resize(image_shape[::-1], Image.ANTIALIAS))
            self.canvas.create_image(0, 0, image=self.canvas.image, anchor="nw")

            # add graph buttons
            self.save_b = tk.Button(self.graph_f, text="Zapisz obraz", command=lambda: self.save_image())
            self.csv_save_b = tk.Button(self.graph_f, text="Zapisz jako csv", command=lambda: self.save_csv())

            self.save_b.grid(row=3, column=image_column)

    def valid_graph(self, entry):
        if entry.get() == '':
            entry.configure(bg='red')
            return False
        entry.configure(bg='white')
        return True

    def remove_widgets(self, *item_list):
        for item in item_list:
            if type(item) is list:
                for i in item:
                    i.destroy()
            else:
                if item is not None:
                    item.destroy()

    def save_image(self):
        image_to_save = Image.open("file.png")
        file = filedialog.asksaveasfile(mode='w', defaultextension=".png",
                                        filetypes=(("PNG file", "*.png"), ("All Files", "*.*")))
        if file:
            abs_file = os.path.abspath(file.name)
            image_to_save.save(abs_file)

    def save_csv(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()
