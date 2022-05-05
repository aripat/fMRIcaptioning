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

data = []
for x in scenes['scene'].values:
    scene = '_'.join(segment(x))
    scene = nltk.pos_tag(nltk.word_tokenize(scene))
    filenames = [file for file in img_filenames if file.startswith(x)]
    candidates = scene.split('_')
    data.append({"scene": scene,
                 "candidates": candidates,
                 "candidates_syn": [wn.synsets(cand, pos='n') for cand in candidates],
                 "synset": wn.synsets(scene, pos='n'),
                 "label": x, "filenames": filenames})

data = pd.DataFrame(data)
data.set_index(["scene"], inplace=True)
print(data.loc['reading_room'])

missing = {}
count = 0
for scene in data.index:
    if len(data.loc[scene]["synset"]) == 0:
        print(scene, data.loc[scene]["synset"], len(data.loc[scene]["synset"]))
        missing[scene] = data.loc[scene]["label"]
        count += 1

print(f"Scene con label che non esistono in wordnet: {count}, {count/250}%")



fig, axes = plt.subplots(10, 8, figsize=(50,50),
                         gridspec_kw={'height_ratios': np.ones(10), 'width_ratios': np.ones(8)})

missing_labels = list(missing.keys())
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

#plt.show()
if not os.path.exists("missing_scenes.png"):
    plt.savefig("missing_scenes.png")

with open('new_labels_scene.txt') as fd:
    labels = fd.readlines()

for l in labels:
    l = l.split('[]')
    for i in range(len(l)):
        l[i] = l[i].strip()
    if len(l[1]) > 1:
        l[1] = (l[1].split("->")[1]).strip()
    else:
        l[1] = l[0]

print(labels)




