import pandas as pd
import itertools
import numpy as np
import requests
import re
import lyricsgenius as genius
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

from IPython.display import HTML, display
from bs4 import BeautifulSoup


key = 'Lyf0cZjy4Tg0zuxSn6oL4X4JpAVswuBmCVZflKg8kk3A0G2Qa0Y2Zkd4AYpiG8PX'
api = genius.Genius(key, sleep_time=0.01, verbose=False)



def get_billboard_songs(years=[2018, 2019, 2020]):
    dataset = []
    for year in years:
        print(year)
        url = "https://www.billboard.com/charts/year-end/" + str(year) + "/hot-100-songs"
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")
        all_ranks = soup.find_all("div", class_="ye-chart-item__rank")
        all_titles = soup.find_all('div', class_="ye-chart-item__title")
        all_artists = soup.find_all("div", class_="ye-chart-item__artist")
        for j in range (0, len(all_ranks)):
            row = {
                "Rank": int(all_ranks[j].get_text(strip=True)),
                "Song Title": all_titles[j].get_text(strip=True),
                "Artist": all_artists[j].get_text(strip=True),
                "Year": int(year)
            }
            dataset.append(row)
    return dataset


def get_lyrics():
    
    songs = get_billboard_songs()
    for i in songs:
        print(i['Song Title'])
        try:
            song = api.search_song(i['Song Title'], artist=i['Artist'])
            i['Lyrics'] = re.sub("\\n", " ", song.lyrics)
            i['Lyrics'] = re.sub(r'\[.*?]', '', i['Lyrics'])
            # print(i['Lyrics'])
            i['Lyrics'] = re.sub('[^A-Za-z0-9]+', ' ', i['Lyrics'])#Remove newline breaks, we won't need them.
        except:
            i['Lyrics'] = "null"
    return songs

def tfidf_features(corpus):
    
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(corpus)
    return X


def create_lyric_list(data):
    songs = []
    for i in data:
        songs.append(i['Lyrics'])
    return songs
    
    
def create_features():
    data = get_lyrics()
    lyrics = create_lyric_list(data)
    
    tfidf = tfidf_features(lyrics)
    
    for i , v in enumerate(tfidf):
        data[i]['tfidf'] = v.toarray()
    
    return data


# def create_combinations():
#     data = create_features()
#     combs = []

#     for i in range(len(data)+1):
#         for sub in  itertools.combinations(data, i):
# #         print(list(els[0]))
#             combs.append(sub)
#     return combs

# print('GO')

combo = get_lyrics()



print(combo)
import json
with open(r'D:\IS688\song_combos.json', 'w') as f:
    f.write(json.dumps(combo))

# from snapy import MinHash, LSH

# content = [
#     'Jupiter is primarily composed of hydrogen with a quarter of its mass '
#     'being helium',
#     'Jupiter moving out of the inner Solar System would have allowed the '
#     'formation of inner planets.',
#     'A helium atom has about four times as much mass as a hydrogen atom, so '
#     'the composition changes when described as the proportion of mass '
#     'contributed by different atoms.',
#     'Jupiter is primarily composed of hydrogen and a quarter of its mass '
#     'being helium',
#     'A helium atom has about four times as much mass as a hydrogen atom and '
#     'the composition changes when described as a proportion of mass '
#     'contributed by different atoms.',
#     'Theoretical models indicate that if Jupiter had much more mass than it '
#     'does at present, it would shrink.',
#     'This process causes Jupiter to shrink by about 2 cm each year.',
#     'Jupiter is mostly composed of hydrogen with a quarter of its mass '
#     'being helium',
#     'The Great Red Spot is large enough to accommodate Earth within its '
#     'boundaries.'
# ]

# labels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# seed = 3


# # Create MinHash object.
# minhash = MinHash(content, n_gram=9, permutations=100, hash_bits=64, seed=3)


# # Create LSH model.
# lsh = LSH(minhash, labels, no_of_bands=50)


# # Query to find near duplicates for text 1.
# print(lsh.query(1, min_jaccard=0.5))


# # Generate minhash signature and add new texts to LSH model.
# new_text = [
#     'Jupiter is primarily composed of hydrogen with a quarter of its mass being '
#     'helium',
#     'Jupiter moving out of the inner Solar System would have allowed the '
#     'formation of inner planets.',
# ]

# new_labels = ['doc1', 'doc2']

# new_minhash = MinHash(new_text, n_gram=9, permutations=100, hash_bits=64, seed=3)

# lsh.update(new_minhash, new_labels)


# # Check contents of documents.
# print(lsh.contains())



# # Remove text and label from model.
# lsh.remove(5)
# print(lsh.contains())



# # Return adjacency list for all similar texts.
# adjacency_list = lsh.adjacency_list(min_jaccard=0.55)
# print(adjacency_list)



# # Returns edge list for use creating a weighted graph.
# edge_list = lsh.edge_list(min_jaccard=0.5, jaccard_weighted=True)
# print(edge_list)



# import networkx as nx

# import matplotlib.pyplot as plt


# g = nx.DiGraph()
# for item in act:

#     g.add_node(item)

# print(len(g.nodes()))


# for index, row in dfg.iterrows():
#     g.add_edge(row['index_actor'], row['related_actors'], weight=int(row['weight']))

# print(len(g.edges()))
# print(g.nodes())
# print(g.edges())
# pos=nx.spring_layout(g)
# nx.draw_networkx(g, pos)
# labels = nx.get_edge_attributes(g,'weight')
# nx.draw_networkx_edge_labels(g,pos,edge_labels=labels, )


# plt.show()  


# for actor in act:
#     g.out_edges(actor)

# between = nx.betweenness_centrality(g)

# framer = []
# for k, v in between.items():

#     new = {}
#     new['Actor'] = k
#     new['Value'] = v
#     framer.append(new)

# bet_df = pd.DataFrame(framer)

# bet_df.sort_values('Value', ascending=False)