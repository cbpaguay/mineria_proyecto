# %%
import pandas as pd
import re
# %%

# sectores
dfs = pd.read_csv("./data/sectores/dpa_.csv")
# dataset completo
df = pd.read_csv("./data/complete_news_dataset.csv")
df = df.dropna()
# %%
sectores = list()

dfp = dfs['NombreProvincia']
dfp = dfp.drop_duplicates()
dfp = dfp.apply(lambda x: x.strip().title())

dfc = dfs['NombreCanton']
dfc = dfc.drop_duplicates()
dfc = dfc.apply(lambda x: x.strip().title())

dfpa = dfs['NombreParroquia']
dfpa = dfpa.drop_duplicates()
dfpa = dfpa.apply(lambda x: x.strip().title())

# funcion para detectar un sector

def find_sector(texto):
    salir = 0
    texto = texto.strip()
    texto = re.sub('[^a-zA-Z]', ' ', texto)
    texto = texto.split(" ")
    for provincia in dfp:
        if provincia in texto:
            sectores.append(provincia)
            salir = 1
            break
    
    if salir == 0:
        for canton in dfc:
            if canton in texto:
                sectores.append(canton)
                salir = 1
                break
 
    if salir == 0:
        for parroquia in dfpa:
            if parroquia in texto:
                sectores.append(parroquia)
                salir = 1
                break

    if salir == 0:
        sectores.append("")
# %%
i = 1
size = len(df.index)
for d in df['descripcion']:
    print(i,"of",size)
    find_sector(d)
    i = i + 1  

df['sector'] = sectores
df.to_csv("./data/dataset_sector.csv", index=False)
