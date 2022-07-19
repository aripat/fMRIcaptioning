"# fMRIcaptioning" 

# 2022/07/19
## Commit id: major update on generated files
::Riordine di idee e di files::

Abbiamo preso le label di scene, mal scritte, le abbiamo segmentate (wordsegment)

Abbiamo cercato quali label esistevano su wordnet, e 82 di queste non esistevano

Tutte queste 82 le abbiamo sistemate:
- divise in spec_concept_adj
- collegato a wordnet i synset dei concept

DA FARE: 
- (sysent spec??)
- Salvare data (sun_scene_categories.py)
- Disambiguare data
- Aggiungere adj a data
- Fare il merge di data e delle missing labels (labels_to_concept)