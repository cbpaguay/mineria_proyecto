# %%
import pandas as pd

# Dataset Fake News 
df = pd.read_csv("./data/fake_news_elmercioco.csv",index_col=['Unnamed: 0'])
df.drop_duplicates(subset=['link'],inplace=True,ignore_index=True)
# %%
# eliminando datos nulos
df.isnull().sum()
df.dropna(subset=['descripcion'],inplace=True)
# %%
# eliminando noticias que son videos,fotos,galeria,audio
cadenas = ["memes","video","foto","fotos","galería","galeria","fotografías","audio"]
to_delete = list()
for desc in df.titulo:
    for c in cadenas:
        if c in desc.lower():
            to_delete.append("si")
            break
        elif c == "audio":
            to_delete.append("no")

df['to_delete'] = to_delete
df.drop(df[df.to_delete == "si"].index,inplace=True)
df.drop(columns=['to_delete'], inplace=True)
df['is_fake'] = 1
df.reset_index(drop=True,inplace=True)
# %%
# extrayendo solo los parrafos
df.descripcion = df.descripcion.apply(lambda x: x.split('.-')[1].strip() if len(x.split('.-')) > 1 else x.split('.-')[0])
linea = "AFP. Noticias. Quito, Ecuador"
df.descripcion = df.descripcion.apply(lambda x: x.split(linea)[1].strip() if len(x.split(linea)) > 1 else x.split(linea)[0])
linea = "APF. Noticias. Quito, Ecuador"
df.descripcion = df.descripcion.apply(lambda x: x.split(linea)[1].strip() if len(x.split(linea)) > 1 else x.split(linea)[0])
linea = "AFP Noticias. Quito, Ecuador"
df.descripcion = df.descripcion.apply(lambda x: x.split(linea)[1].strip() if len(x.split(linea)) > 1 else x.split(linea)[0])
linea = "APF Noticias. Quito, Ecuador"
df.descripcion = df.descripcion.apply(lambda x: x.split(linea)[1].strip() if len(x.split(linea)) > 1 else x.split(linea)[0])
linea = "AFP Noticias, Quito, Ecuador"
df.descripcion = df.descripcion.apply(lambda x: x.split(linea)[1].strip() if len(x.split(linea)) > 1 else x.split(linea)[0])
linea = "APF Noticias, Quito, Ecuador"
df.descripcion = df.descripcion.apply(lambda x: x.split(linea)[1].strip() if len(x.split(linea)) > 1 else x.split(linea)[0])
# %%
cadenas = ["APS","AFS","AFP","APF"]
to_delete = list()
for desc in df.descripcion:
    for c in cadenas:
        if c in desc:
            to_delete.append("si")
            break
        elif c == "APF":
            to_delete.append("no")

df['to_delete'] = to_delete
df.drop(df[df.to_delete == "si"].index,inplace=True)
df.drop(columns=['to_delete'], inplace=True)
# %%
# eliminando noticias con contenidos de pocas palabras
df['to_delete'] = df.descripcion.apply(lambda x: True if len(x) < 150 else False)
df.drop(df[df.to_delete == True].index,inplace=True)
df.drop(columns=['to_delete'], inplace=True)
# %%
# Dataset el nuevo
df.to_csv("./data/complete_dataset_1.csv",index=False)