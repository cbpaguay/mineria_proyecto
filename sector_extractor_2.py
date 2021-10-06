# %%
import pandas as pd
import re
import spacy
# %%
df = pd.read_csv("./data/complete_news_dataset.csv")
df = df.dropna()
# %%
nlp = spacy.load("es_dep_news_trf")
doc = nlp("Esto es una frase.")
print([(w.text, w.pos_) for w in doc])