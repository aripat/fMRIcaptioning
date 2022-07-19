import os
import pandas as pd
import matplotlib.pyplot as plt
import json

stimuli_dir = os.path.join('bold5000', 'stimuli', 'Image_Labels')
annotation_dir = os.path.join('bold5000', 'annotations')

coco_categories = pd.read_csv('cococat.csv', names=['category_name'], header=None)['category_name'].values

labels = {}
count_obj_by_image = {}
ids = {}

name = "coco_final_annotations.pkl"
pdata = pd.read_pickle(os.path.join(stimuli_dir, name))
rdata = []
for i in pdata:
    image = pdata[i]
    print(image)
    for obj in image:
        label = coco_categories[int(obj['category_id'])]
        rdata.append(label)
    ids[image[0]['image_id']] = 1

    if len(image) not in count_obj_by_image:
        count_obj_by_image[len(image)] = []
    count_obj_by_image[len(image)].append(image[0]['image_id'])

fd = open(os.path.join(annotation_dir, 'coco_2017', 'captions_train2017.json'), 'r')
annotations = json.load(fd)
fd.close()
# annotations has dict_keys(['info', 'licenses', 'images', 'annotations'])
annotations_ids = {image['id']: 1 for image in annotations['images']}

found = True
for i in ids:
    if i not in annotations_ids:
        found = False
print(found)


