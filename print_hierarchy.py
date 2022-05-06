import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import wordnet as wn

syns = pd.read_csv('elena_new_labels_scene_definitions.csv')
syns = syns[syns['syn_chosen_concept'].notna()]['syn_chosen_concept']
hierarchy = []
nodes = []
links = {}
for syn in syns.values:
    hypers = [x.name() for x in reversed(wn.synset(syn).hypernym_paths()[0])]
    nodes.extend(hypers)

    for i in range(len(hypers) - 1):
        if hypers[i] not in links:
            links[hypers[i]] = []
        links[hypers[i]].append(hypers[i+1])


G = nx.from_dict_of_lists(links)
nx.draw(G, with_labels=True)
plt.show()