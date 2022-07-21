import os

import pandas as pd
import nltk
import numpy as np
from nltk.corpus import wordnet as wn
import pandas as pd
from wordsegment import load, segment
from matplotlib import pyplot as plt

load()

# nltk.download('wordnet')
# nltk.download('omw-1.4')

labels_dir = os.path.join('bold5000', 'stimuli', 'Image_Labels')
images_dir = os.path.join('bold5000', 'stimuli', 'Scene_Stimuli', 'Presented_Stimuli', 'Scene')

scenes = pd.read_csv(os.path.join(labels_dir, 'scene_final_labels.txt'), names=['scene'])

img_filenames = os.listdir(images_dir)

# Noi abbiamo applicato il segment perché la struttura delle label
# non era ben definita; ora avremo tutte le parole separate
# da underscore, in linea con la rappresentazione di wordnet in nltk

data = []
for x in scenes['scene'].values:
    segmented = '_'.join(segment(x))
    # scene = nltk.pos_tag(nltk.word_tokenize(scene))

    filenames = [file for file in img_filenames if file.startswith(x)]
    candidates = segmented.split('_')
    data.append({"original": x,
                 "segmented": segmented,
                 "filenames": filenames})

data = pd.DataFrame(data)
data.set_index(["segmented"], inplace=True)

# scrittura delle labels segmentate (tutte) che verrà ritoccata a mano
# per ottenere quella delle labels ben segmentate
# & con mappatura (+) di sintagmi su wordnet (scene_labels/segmented_labels_scene.txt)

rows = []
for segmented in data.index:
    rows.append(segmented)

if not os.path.exists('scene_labels/provvisorio_labels_scene.txt'):
    f = open('scene_labels/provvisorio_labels_scene.txt', 'w+')
    f.writelines("%s\n" % r for r in rows)

# modifichiamo data con le labels ben segmentate

with open('scene_labels/segmented_labels_scene.txt') as f:
    corr_labels = f.read().splitlines()
    i = 0

data.index = corr_labels

# Osserviamo quante e quali label non hanno corrispettivo con wordnet
# sono 82

missing_labels = []
count = 0

rows = []
for label in data.index:
    if len(wn.synsets(label, pos='n')) == 0:
        rows.append(label)
        missing_labels.append(label)
        count += 1

if not os.path.exists('scene_labels/new_labels_scene.txt'):
    f = open('scene_labels/new_labels_scene.txt', 'w+')
    f.writelines(rows)

print(f"Scene con label che non esistono in wordnet: {count}, {count / len(data.index)}%")

# plot di esempi delle scene mancanti, utili per mappare in modo coerente
# le vecchie labal su wordnet

fig, axes = plt.subplots(10, 8, figsize=(50,50),
                         gridspec_kw={'height_ratios': np.ones(10), 'width_ratios': np.ones(8)})

for i in range(0, 10):
    for j in range(0, 8):
        filename = data.loc[missing_labels[8*i+j]]["filenames"][0]
        path = os.path.join(images_dir, filename)
        im = plt.imread(path)
        axes[i][j].imshow(im, extent=[0, 300, 0, 300])
        axes[i][j].set_xticklabels([])
        axes[i][j].set_yticklabels([])
        axes[i][j].title.set_text(filename)

plt.subplots_adjust(wspace=0)

if not os.path.exists("stats_analysis/missing_scenes.png"):
    plt.savefig("stats_analysis/missing_scenes.png")

# a mano abbiamo mappato le 82 label non esistenti su wordnet
# NB: per i concetti complessi abbiamo adottato la struttura spec_concept
# (esempio: hotel_room, city_street)
# abbiamo poi aggiunto l'aggettivo outdoor/indoor/interior/exterior
# !!!!! qua abbiamo usato la colonna "original" in modo improprio, perché sono già segmentate


# nuove label definitive -> new_labels_scene.csv

# modifichiamo il dataframe sostituendo le 82 anomalie
# con le nuove labels mappate su wordnet

new_labels = pd.read_csv('scene_labels/new_labels_scene.csv', index_col=False)

for label in new_labels['original'].values:
    new_label, = new_labels[new_labels['original'] == label]['new'].values
    data.rename(index={label: new_label}, inplace=True)
    print(label + ' -> ' + new_label)

# creiamo la lista delle labels finali mappate du wordnet

rows = []
for label in data.index:
    rows.append(label)

if not os.path.exists('scene_labels/wordnet_scene_final_labels.txt'):
    f = open('scene_labels/wordnet_scene_final_labels.txt', 'w+')
    f.writelines("%s\n" % r for r in rows)

# scrittura dei dati secondo l'idea spec_concept_adj
# data: (label), original, filenames
# TODO da fare dopo aver fatto a parte la disambiguazione e il merge

adj = {'outdoor': 1, 'indoor': 1, 'exterior': 1, 'interior': 1}
keys = ['original', 'new', 'spec', 'concept', 'adj', 'chosen_syn_spec', 'chosen_syn_concept']

struct = []
for label in data.index:

    parts = label.split('_')

    if parts[-1] not in adj:
        # non  c'è l'aggettivo
        parts.append('')

    if len(parts) == 2:
        # non c'è la specificazione
        parts.insert(0, '')

    dict = {
        'original': data.loc[label]['original'],
        'new': label,
        'spec': parts[0],
        'concept': parts[1],
        'adj': parts[2]
    }





