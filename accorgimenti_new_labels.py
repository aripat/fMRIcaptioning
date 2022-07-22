import pandas as pd

# modifico 'new_labels_with_syn_concept_scene.csv' con il label come index
# per sicurezza lo ho copiato e chiamato 'new_chosen_concept_scene.csv'

# ,spec,concept,syn_concept,syn_chosen_concept,def_chosen_concept
df = pd.read_csv('scene_labels/new_chosen_concept_scene.csv', index_col=False)

df.drop(['Unnamed: 0'], axis=1, inplace=True)

with open('scene_labels/wordnet_scene_final_labels.txt', 'r+') as f:
    labels = f.read().splitlines()

for i in df.index:
    df.loc[i]['concept'] = df.loc[i]['concept'].replace('_', '+')
    new_label = df.loc[i]['concept']
    if not df.isnull().loc[i]['spec']:
        df.loc[i]['spec'] = df.loc[i]['spec'].replace('_', '+')
        new_label = df.loc[i]['spec'] + '_' + new_label
    for true_label in labels:
        if true_label.startswith(new_label):
            df.rename(index={i: true_label}, inplace=True)

df.to_csv('scene_labels/new_chosen_concept_scene.csv')


