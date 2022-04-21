import os

import pandas
from nltk.corpus import wordnet as wn
import pandas as pd
from wordsegment import load, segment
load()

stimuli_dir = os.path.join('bold5000', 'stimuli', 'Image_Labels')
scenes = pd.read_csv(os.path.join(stimuli_dir, 'scene_final_labels.txt'), names=['scene'])

synset = {}
for x in scenes['scene'].values:
    scene = '_'.join(segment(x))
    synset[scene] = wn.synsets(scene, pos='n')


for scene in synset:
    if len(synset[scene]) == 0:
        print(scene, synset[scene], len(synset[scene]))
