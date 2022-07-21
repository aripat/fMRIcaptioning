import pandas as pd

# scelta del synset per il concept

# modifico 'new_labels_with_syn_concept_scene.csv' con il label come index
# per sicurezza lo ho copiato e chiamato 'new_chosen_concept_scene.csv'

# ,spec,concept,syn_concept,syn_chosen_concept,def_chosen_concept
df = pd.read_csv('scene_labels/new_chosen_concept_scene.csv', index_col=False)

with open('scene_labels/wordnet_scene_final_labels.txt', 'r+') as f:
    labels = f.read().splitlines()

df.fillna('')

for i in df.index:
    print(df.loc[i])
    new_label = df.loc[i]['concept'].replace('')
    if not df.isnull().loc[i]['spec']:
        new_label = df.loc[i]['spec'] + '_' + new_label
    for true_label in labels:
        if true_label.startswith(new_label):
            df.rename(index={i: true_label}, inplace=True)

print(list(df.index))

