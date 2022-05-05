import pandas as pd
import numpy as np
import os
from nltk.corpus import wordnet as wn

with open('new_labels_scene.txt') as fd:
    labels = fd.readlines()

for j in range(len(labels)):
    l = labels[j].split('[]')
    for i in range(len(l)):
        l[i] = l[i].strip()
    if len(l[1]) > 1:
        l[1] = (l[1].split("->")[1]).strip()
    else:
        l[1] = l[0]

    labels[j] = l

labels = np.array(labels, dtype=object)

adj = {'outdoor':1, 'indoor':1, 'exterior':1, 'interior':1}
keys = ['original', 'new', 'spec', 'concept', 'adj', 'syn_spec', 'syn_concept']

data = []

for i in range(len(labels)):
    dict = {keys[0]: labels[i, 0],
            keys[1]: labels[i, 1]}

    l = labels[i, 1].split('_')
    if l[-1] not in adj:
        l.append('')
    if len(l) == 2:
        l.insert(0, '')

    for j in range(len(l)):
        dict[keys[j+2]] = l[j].replace('+', '_')

    dict['syn_spec'] = wn.synsets(dict['spec'], pos=['n', 'a'])
    dict['syn_concept'] = wn.synsets(dict['concept'], pos='n')

    data.append(dict)

data = pd.DataFrame(data)

#if not os.path.exists('new_labels_scene.csv'):
data.to_csv('new_labels_scene.csv')

print(data['syn_concept'].values)

