import datetime
from datetime import date

from bokeh.io import curdoc
from bokeh.layouts import column, layout, row
from bokeh.models import Select, DatePicker, TextInput, Button, TableColumn, DataTable

import numpy as np
import networkx as nx
import twint

from bokeh.models import Circle, MultiLine
from bokeh.plotting import figure, from_networkx, show
from bokeh.models import ColumnDataSource
from bokeh.transform import dodge
from numpy.random import randint
import pandas as pd
import nest_asyncio
nest_asyncio.apply()

class Dashboard:
    """
    main dashboard class with class members for dashboard global variables which can be changed by callbacks
    """

    def __init__(self,
                 active_window_size=7,
                 ):
        # global variables which can be controlled by interactive bokeh elements
        self.active_window_size = active_window_size
        self.layout = None

    opt = ['0', '100', '200', '300', '400', '500', '600', '700', '800', '900', '1000', '1100',
           '1200', '1300', '1400', '1500', '1600', '1700', '1800', '1900', '2000', '2100', '2200',
           '2300', '2400', '2500', '2600', '2700', '2800', '2900', '3000']
    username = TextInput(title="Nazwa użytkownika")
    search_word = TextInput(title="Poszukiwane słowo")
    date_from = DatePicker(title="Data początkowa", value=date.today() - datetime.timedelta(days=30))
    date_until = DatePicker(title="Data końcowa", value=date.today())
    num_of_tweets = Select(title="Liczba tweetow", value='0', options=opt)
    p = None
    q = None
    r = None
    s = None
    columns = None
    def get_tweets(self):   #wczytanie tweetów
        try:                        #w przeciwnym razie konfigurujemy Twinta
            c = twint.Config()
            c.Username = self.username.value
            c.Limit = self.num_of_tweets.value
            c.Pandas = True
            c.Retweets = True
            c.Pandas_clean = True
            c.Stats = True
            c.Count = True
            c.Since = self.date_from.value
            c.Until = self.date_until.value
            c.Search = self.search_word.value
            c.Hide_output = True
            twint.run.Profile(c)
            if twint.output.panda.Tweets_df.empty:    #jeśli nie znaleziono tweetów to informujemy o tym
                print("No tweets from user: ", self.username.value)
                return twint.output.panda.Tweets_df
            else:                                     #zwracamy pustą lub pełną ramke danych
                return twint.output.panda.Tweets_df
        except ValueError:                     #obsługujemy potencjalne wyjątki
            print("Get tweets - Blad wartosci, user:", self.username.value)
            return pd.DataFrame()
        except Exception as exc:
            print("Get tweets - Cos poszlo nie tak, user: {user}, wyjatek: {excType} {excMsg}"
                  .format(user=self.username.value, excType=type(exc).__name__, excMsg=str(exc)))
            return pd.DataFrame()

    def refresh(self):
        source = ColumnDataSource(self.get_tweets())
        new_graph4 = DataTable(source=source, columns=self.columns, width=500, height=280, editable=False)
        self.layout = layout([
            row(column(self.p, self.q),
                column(self.r, new_graph4),
                column(self.username, self.search_word, self.date_from, self.date_until, self.num_of_tweets,
                       row(self.refresh_button, self.export_button)
                       ))
        ])

    def save_to_csv(self):
        print("Zapisywanie!")


    def generate_figures(self):
        x = np.linspace(0, 4 * np.pi, 100)
        y = np.sin(x)
        p = figure(title="Legend Example")
        p.circle(x, y, legend_label="sin(x)")
        p.circle(x, 2 * y, legend_label="2*sin(x)", color="orange")
        p.circle(x, 3 * y, legend_label="3*sin(x)", color="green")
        p.legend.title = 'Markers'
        G = nx.karate_club_graph()

        SAME_CLUB_COLOR, DIFFERENT_CLUB_COLOR = "darkgrey", "red"

        edge_attrs = {}
        for start_node, end_node, _ in G.edges(data=True):
            edge_color = SAME_CLUB_COLOR if G.nodes[start_node]["club"] == G.nodes[end_node][
                "club"] else DIFFERENT_CLUB_COLOR
            edge_attrs[(start_node, end_node)] = edge_color

        nx.set_edge_attributes(G, edge_attrs, "edge_color")

        q = figure(width=400, height=400, x_range=(-1.2, 1.2), y_range=(-1.2, 1.2),
                      x_axis_location=None, y_axis_location=None, toolbar_location=None,
                      title="Graph Interaction Demo", background_fill_color="#efefef",
                      tooltips="index: @index, club: @club")
        q.grid.grid_line_color = None

        graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
        graph_renderer.node_renderer.glyph = Circle(size=15, fill_color="lightblue")
        graph_renderer.edge_renderer.glyph = MultiLine(line_color="edge_color",
                                                       line_alpha=0.8, line_width=1.5)
        q.renderers.append(graph_renderer)
        fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
        years = ['2015', '2016', '2017']

        data = {'fruits': fruits,
                '2015': [2, 1, 4, 3, 2, 4],
                '2016': [5, 3, 3, 2, 4, 6],
                '2017': [3, 2, 4, 4, 5, 3]}

        source = ColumnDataSource(data=data)

        r = figure(x_range=fruits, y_range=(0, 10), title="Fruit Counts by Year",
                   height=350, toolbar_location=None, tools="")

        r.vbar(x=dodge('fruits', -0.25, range=r.x_range), top='2015', source=source,
               width=0.2, color="#c9d9d3", legend_label="2015")

        r.vbar(x=dodge('fruits', 0.0, range=r.x_range), top='2016', source=source,
               width=0.2, color="#718dbf", legend_label="2016")

        r.vbar(x=dodge('fruits', 0.25, range=r.x_range), top='2017', source=source,
               width=0.2, color="#e84d60", legend_label="2017")

        r.x_range.range_padding = 0.1
        r.xgrid.grid_line_color = None
        r.legend.location = "top_left"
        r.legend.orientation = "horizontal"
        data1 = pd.read_csv("donaldtusk.csv")
        source = ColumnDataSource(data1)

        self.columns = [
            TableColumn(field="id", title="ID"),
            TableColumn(field="tweet", title="Tekst"),
        ]
        s = DataTable(source=source, columns=self.columns, width=400, height=280, editable=False)
        return [p, q, r, s]
    def do_layout(self):
        """
        generates the overall layout by creating all the widgets, buttons etc and arranges
        them in rows and columns
        :return: None
        """
        wordcloud_g = None
        interconnections_g = None
        statistics_g = None
        tweet_l = None
        refresh_button = Button(label="Załaduj tweety", button_type="default", width=150)
        refresh_button.on_event('button_click', self.refresh)
        export_button = Button(label="Zapisz do CSV", button_type="default", width=150)
        export_button.on_event('button_click', self.save_to_csv)
        p, q, r, s = self.generate_figures()
        self.layout = layout([
            row(column(p, q),
                column(r, s),
                column(self.username, self.search_word, self.date_from, self.date_until, self.num_of_tweets,
                       row(refresh_button, export_button)
                       ))
        ])
        curdoc().add_root(self.layout)
        curdoc().title = "Przykładowy dashboard"


dash = Dashboard()
dash.do_layout()