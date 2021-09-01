# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
titulo = list()
link = list()
# aplicar cada tag y el número de páginas
tags = {"tag": "asalto", "paginas": 19}
# %%
url = "https://www.eltelegrafo.com.ec/contenido/etiqueta/12/{}".format(
    tags['tag'])
# %%
for i in range(1, tags['paginas']):  # actualmente son 142 paginas
    if(i == 1):
        url = "https://www.eltelegrafo.com.ec/contenido/etiqueta/12/{}".format(
            tags['tag'])
    else:
        url = "https://www.eltelegrafo.com.ec/contenido/etiqueta/12/{}?start={}".format(
            tags['tag'], (i*10)-10)
    print("Page:", i)
    page = requests.get(url, timeout=10.500)  # obtengo la pagina entera
    soup = BeautifulSoup(page.content, 'html.parser')
    for anchor in soup.select('h1.story-heading'):
        link.append(anchor.find('a')['href'])
        titulo.append(anchor.find('a').text)

    indices = [i for i, s in enumerate(link) if 'columnistas' in s]
    if(len(indices) > 0):
        print("Indice ", indices[0])
        link.pop(indices[0])
        titulo.pop(indices[0])
        
    del(indices)


df = pd.DataFrame(columns=['titulo', 'link'])
df['titulo'] = titulo
df['link'] = link
# %%
#Remover duplicados
df.drop_duplicates(subset=None, keep="first", inplace=True)
#Resetear indices
df.reset_index(drop=True)
# Exportar los datos a un csv
df.to_csv('./data/{}_eltelegrafo.csv'.format(tags['tag']), sep=',')
