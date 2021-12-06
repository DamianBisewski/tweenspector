import tkinter as tk
import igraph as ig
import matplotlib.pyplot as plt

from App_variables import *
from FeatureStrategy import FeatureStrategy


class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.configure(background=bg)
        self.parent.geometry('500x450')
        self.parent.title('Searched phrases on Twitter')
        self.parent.resizable(False, False)

        self.nav_f, self.act_f = None, None  # frames
        self.nav_b, self.act_b = [], []  # buttons
        self.nav_l, self.act_l = None, []  # labels
        self.act_e = []  # entries
        self.act_lb = None  # listbox
        self.act_s = None  # scroll
        # program feature
        self.feature_strategy = None
        # start page
        self.StartPage()

    def StartPage(self):
        self.prepare_start_page()

        self.nav_f = tk.Frame(self.parent, bg=bg)
        self.nav_f.grid(row=1, column=1, rowspan=4, columnspan=3, pady=(20, 100))

        self.nav_l = tk.Label(self.nav_f, text='Dostępne operacje na użytkownikach Twittera', bg=bg, font=large_font,
                              fg='white')
        self.nav_l.grid(row=1, column=1, pady=(20, 0))

        self.nav_b = [tk.Button(self.nav_f, text='Lista powiązanych słów',
                                command=self.related_words, font=large_font),
                      tk.Button(self.nav_f, text='Powiązani korespondenci',
                                command=self.related_people, font=large_font),
                      tk.Button(self.nav_f, text='Temat kont użytkowników',
                                command=self.users_search_by_subject, font=large_font)]
        for i in range(len(self.nav_b)):
            self.nav_b[i].configure(width=25, padx=30, pady=5)
            self.nav_b[i].grid(row=i + 2, column=1, padx=90, pady=(20, 0))

    def set_action_frame(self, feature):
        self.feature_strategy = FeatureStrategy(feature)

        self.act_f = tk.Frame(self.parent, height=600, bg=bg)

        self.act_e = [tk.Entry(self.act_f, width=25, font=small_font)]  # topic or user input
        self.act_e.append(tk.Entry(self.act_f, width=25, font=small_font))  # max nodes input
        self.act_e.append(tk.Entry(self.act_f, width=25, font=small_font))  # precision 1-100

        self.act_b = [tk.Button(self.act_f, text='Wyszukaj', command=lambda: self.search_result())]
        self.act_b.append(tk.Button(self.act_f, text='Powrót', command=lambda: self.StartPage()))

        self.act_s = tk.Scrollbar(self.act_f, orient='vertical')
        self.act_lb = tk.Listbox(self.act_f, yscrollcommand=self.act_s.set, height=14)
        self.act_s.config(command=self.act_lb.yview)

        self.act_l = [tk.Label(self.act_f, text=self.feature_strategy.feature.set_graph_item(),
                               bg=bg, fg='white', font=large_font)]
        self.act_l.append(tk.Label(self.act_f, text='Wierzchołki grafu 3-999', bg=bg, fg='white',
                                   font=large_font))
        self.act_l.append(tk.Label(self.act_f, text='Dokładność: 1-100', bg=bg, fg='white', font=large_font))

        self.act_l.append(tk.Label(self.act_f, bg=bg, fg='white',
                                   text=self.feature_strategy.feature.set_text_listbox_label(), font=large_font))
        for item in self.feature_strategy.feature.set_listbox():
            print('item', item)
            self.act_lb.insert(tk.END, item)

    def grid_action_frame(self):
        self.act_f.grid(row=1, column=1, columnspan=3, rowspan=3, padx=(50, 0), pady=(50, 0), sticky='nw')

        self.act_e[0].grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(0, 30))
        self.act_e[1].grid(row=5, column=1, columnspan=2, padx=(20, 0), pady=(0, 30))
        self.act_e[2].grid(row=7, column=1, columnspan=2, padx=(20, 0), pady=(0, 30))

        self.act_b[0].grid(row=8, column=1, pady=0, sticky='nw')
        self.act_b[1].grid(row=1, column=1, pady=(0, 50), sticky='nw')

        self.act_l[0].grid(row=2, column=1, sticky='nw')
        self.act_l[1].grid(row=4, column=1, sticky='nw')
        self.act_l[2].grid(row=6, column=1, sticky='nw')
        self.act_l[3].grid(row=2, column=3, padx=(70, 0))

        self.act_lb.grid(row=3, column=3, rowspan=5, padx=(70, 0), sticky='ne')
        self.act_s.grid(row=3, column=4, rowspan=5, sticky='ns')

    def search_result(self):
        text_input = self.act_e[0].get()
        vertex_count = self.act_e[1].get()
        precision = self.act_e[2].get()

        valid_graph = True

        for entry in self.act_e:
            valid_graph = self.valid_graph(entry)

        try:
            vertex_count = int(vertex_count)
            if (vertex_count < 3) or (vertex_count > 999):
                self.act_e[1].configure(bg='red')
                valid_graph = False
        except ValueError:
            self.act_e[1].configure(bg='red')
            valid_graph = False

        try:
            precision = int(precision)
            if (precision < 1) or (precision > 100):
                self.act_e[2].configure(bg='red')
                valid_graph = False
        except ValueError:
            self.act_e[2].configure(bg='red')
            valid_graph = False

        if self.feature_strategy.feature.is_item_in_list(text_input) is False:
            self.act_e[0].configure(bg='red')
            valid_graph = False

        if valid_graph:
            edges = self.feature_strategy.feature.get_graph_edges(text_input, precision)
            vertices_dictionary = self.feature_strategy.feature.get_vertices_dictionary(text_input)

            g = ig.Graph(edges=edges)
            plt.figure(figsize=(7, 7)), plt.axis('off')
            plt.suptitle(self.feature_strategy.feature.get_graph_title() + ' ' + text_input + ' ' + 'z dokładnością' +
                         ' ' + str(precision) + '%')
            ig.plot(g, target=plt.subplot(111), vertex_size=10,
                    vertex_color=['green'],
                    vertex_label=vertices_dictionary, edge_width=2, margin=50, vertex_label_size=15,
                    vertex_label_dist=1)
            plt.show()

    def valid_graph(self, entry):
        if entry.get() == '':
            entry.configure(bg='red')
            return False
        entry.configure(bg='white')
        return True

    # analiza treści postów danego użytkownika
    def related_words(self):
        self.prepare_graph_page()
        self.set_action_frame(features[0])
        self.grid_action_frame()

    # rekomendacja podobnych kont na podstawie treści
    def related_people(self):
        self.prepare_graph_page()
        self.set_action_frame(features[1])
        self.grid_action_frame()

    # wyszukanie użytkowników najczęściej piszących na dany temat
    def users_search_by_subject(self):
        self.prepare_graph_page()
        self.set_action_frame(features[2])
        self.grid_action_frame()

    def prepare_start_page(self):
        self.remove_widgets(self.act_b, self.act_e, self.act_l, self.act_f, self.act_lb, self.act_s)

    def prepare_graph_page(self):
        self.remove_widgets(self.nav_f, self.nav_b)

    def remove_widgets(self, *item_list):
        for item in item_list:
            if type(item) is list:
                for i in item:
                    i.destroy()
            else:
                if item is not None:
                    item.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()
