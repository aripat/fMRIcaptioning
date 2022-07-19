import os
import pandas as pd
from wordcloud import WordCloud

import matplotlib.pyplot as plt

stimuli_dir = os.path.join('bold5000', 'stimuli', 'Image_Labels')

coco_categories = pd.read_csv('cococat.csv', names=['category_name'], header=None)['category_name'].values

labels = {}
count_obj_by_image = {}

for name in os.listdir(stimuli_dir):
    p = os.path.join(stimuli_dir, name)

    if '.pkl' in name:
        pdata = pd.read_pickle(p)
        print(pdata)
        rdata = []
        for i in pdata:
            image = pdata[i]
            for obj in image:
                label = coco_categories[int(obj['category_id'])]
                rdata.append(label)

            if len(image) not in count_obj_by_image:
                count_obj_by_image[len(image)] = []
            count_obj_by_image[len(image)].append(image[0]['image_id'])

    else:
        if 'scene' in name:
            rdata = pd.read_csv(p, names=['category'], header=None)['category'].values
        else:
            with open(p, "r") as f:
                lines = f.readlines()
                rdata = [x.strip() for line in lines for x in line[9:].split(',')]

    data = {}
    for label in rdata:
        if label not in data:
            data[label] = 0
        data[label] += 1
    labels[name.split('.')[0]] = data


name = 'coco_final_annotations'
words = dict(sorted(labels[name].items(), key=lambda item: item[1], reverse=True))
print(words)
wordcloud = WordCloud(width=1500, height=500, background_color='white').fit_words(words)
# Display the generated image:
plt.figure(figsize=(25, 7), dpi=200)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig("wordcloud_"+name)
plt.close()

x = [str(key) for key in words][1:]
plt.figure(figsize=(15, 7), dpi=300)
plt.bar(x=x, height=[words[key] for key in words][1:])
plt.subplots_adjust(top=1, bottom=0.25)
plt.xticks(rotation='vertical')
plt.savefig("barplot_"+name)
plt.close()


x = [key for key in count_obj_by_image]
plt.figure(figsize=(15, 7), dpi=300)
plt.bar(x=x, height=[len(count_obj_by_image[key]) for key in count_obj_by_image])
plt.savefig("barplot_num_obj_per_image_"+name)
plt.close()

for key in sorted(count_obj_by_image.keys(), reverse=True):
    print(key, count_obj_by_image[key])