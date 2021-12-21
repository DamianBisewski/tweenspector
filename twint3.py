import networkx as nx
import pandas as pd
import numpy as np
import re
import igraph

g = igraph.Graph()
# Read in the tweets
usr = input("Podaj nazwę użytkownika: ")
file_in = usr+'_tweets.csv'
df = pd.read_csv(file_in)
# replace NaN's with an empty string
df = df.replace(np.nan, '')
users = set()
rtsmts = set()
rtsmts.add(usr)
g.add_vertices(1)
G_retweet = nx.DiGraph()
G_mention = nx.DiGraph()
for r in df.iterrows():
    author = r[1]['username']
    author = f'@{author}'
    text = r[1]['tweet']
    #try:
    #    timestamp = pd.to_datetime(r[1]['created_at'])
    #except:
    #    continue
    # use regular expressions to extract retweets and mentions
    rts = set(re.findall(r"RT @(\w+)", text))
    mts = set(re.findall(r"@(\w+)", text))
    for rt in rts:
        rt = rt.lower()
        rtsmts.add(rt)
    for mt in mts:
        mt = mt.lower()
        rtsmts.add(mt)

    # add the users if there are any mentioned in the text.
    #has_users = len(retweets) + len(mentions) > 0
    #if has_users:
    #    for u in retweets:
    #        u = f'@{u}'
            #G_retweet.add_edge(author, u, Timestamp=timestamp)

    #    for u in mentions:
    #        u = f'@{u}'
            #G_mention.add_edge(author, u, Timestamp=timestamp
num = len(rtsmts)
g.add_vertices(num-1)
g.vs["name"] = rtsmts
interactions = list(rtsmts)
x = 0
for i in range(0, num):
    if(interactions[i] == usr):
        x = i
for i in range(0, num):
    if x != i:
        g.add_edges([(x, i)])
print(g)
layout = g.layout("drl")
igraph.plot(g, layout=layout, vertex_label = rtsmts, bbox=(1500, 900), margin = 30, vertex_label_dist = 2, vertex_size = 3)

df_retweet = nx.to_pandas_edgelist(G_retweet)
df_retweet.to_csv('retweet.csv', index=False)

df_mention = nx.to_pandas_edgelist(G_mention)
df_mention.to_csv('mention.csv', index=False)
