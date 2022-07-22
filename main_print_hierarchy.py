from collections import deque

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import wordnet as wn
import os

from nltk.corpus.reader import res_similarity
from nltk.corpus import wordnet_ic
ic_semcor = wordnet_ic.ic('ic-semcor.dat')


def hyper(node):
    hypers = []
    hypernym_paths = wn.synset(node).hypernym_paths()
    for path in hypernym_paths:
        if len(path) > 1:
            hypers.append(path[-2].name())
    return hypers


def criterion(node, syns):
    m = None
    value = 0
    for hyper in syns:
        print(hyper)
        print(node)
        v = wn.synset(node).res_similarity(wn.synset(hyper), ic_semcor)
        if v >= value:
            value = v
            m = hyper
    return m


syns = pd.read_csv('dataset.csv')
leaves = syns[syns['syn_chosen_concept'].notna()]['syn_chosen_concept'].values

# chi e' hyper di chi?
adj = dict()
q = deque([x for x in leaves])
while len(q) > 0:
    node = q.pop()

    hypers = hyper(node)
    if len(hypers) > 0:
        h = criterion(node, hypers)

        if h not in adj:
            adj[h] = {}
        adj[h][node] = 1
        q.append(h)


for node in list(adj.keys()):
    hypos = [x for x in adj[node].keys()]
    if len(hypos) == 1:
        hypo = hypos[0]

        for other in list(adj.keys()):
            if node != other and other not in leaves and node in adj[other]:
                adj[other].pop(node)
                adj[other][hypo] = 1

        adj.pop(node)


links = {n: list(adj[n].keys()) for n in adj}
G = nx.from_dict_of_lists(adj)
nx.draw(G, with_labels=True)
plt.show()
