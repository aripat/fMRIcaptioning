import pandas as pd
import numpy as np
import os
from nltk.corpus import wordnet as wn

with open('scene_labels/new_labels_scene.txt') as fd:
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

# creazione dataframe delle label

adj = {'outdoor':1, 'indoor':1, 'exterior':1, 'interior':1}
keys = ['original', 'new', 'spec', 'concept', 'adj', 'syn_spec', 'syn_concept']

data_labels = []

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

    dict['syn_spec'] = [x.name() for x in wn.synsets(dict['spec'], pos=['n', 'a'])]
    dict['syn_concept'] = [x.name() for x in  wn.synsets(dict['concept'], pos='n')]

    data_labels.append(dict)

data_labels = pd.DataFrame(data_labels)

if not os.path.exists('scene_labels/new_labels_scene.csv'):
    data_labels.to_csv('scene_labels/new_labels_scene.csv')

"""# creazione dataframe con tutti i synset e quelli scelti

data_synset = []

keys = ['spec', 'concept', 'syn_spec', 'syn_concept', 'def_concept', 'chosen_concept', 'syn_chosen_concept']

for i in range(len(labels)):
    dict = {'spec': data_labels['spec'].values[i],
            'concept': data_labels['concept'].values[i]}

    dict['syn_concept'] = [x.name() for x in wn.synsets(dict['concept'], pos='n')]

    dict['syn_chosen_concept'] = []
    dict['def_chosen_concept'] = []

    if len(dict['syn_concept']) == 1:
        dict['syn_chosen_concept'] = dict['syn_concept']
        dict['def_chosen_concept'] = [wn.synset(dict['syn_concept'][0]).definition()]

    data_synset.append(dict)

data_synset = pd.DataFrame(data_synset)

if not os.path.exists('new_labels_with_syn_concept_scene.csv'):
    data_synset.to_csv('new_labels_with_syn_concept_scene.csv')"""


