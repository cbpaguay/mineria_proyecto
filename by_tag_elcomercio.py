# %%
from bs4 import BeautifulSoup
import requests
import pandas as pd
#%% [markdown]
## WEB SCRAPING ROBOS EL COMERCIO
df = pd.DataFrame()
fecha = list()
titulo = list()
desc = list()
# aplicar cada tag y el número de páginas
tags = {"tag":"asalto","paginas":73}
# %%
for i in range(1,tags['paginas']): # actualmente son 142 paginas
    url = "https://www.elcomercio.com/tag/{}/page/{}/".format(tags['tag'],i)
    print("Page:",i)
    page = requests.get(url,timeout=3.500) # obtengo la pagina entera
    soup = BeautifulSoup(page.content, 'html.parser')
    list_item = soup.find_all("div",{"class":"list-item"}) # busco por la clase list-item
# %%
    for l in list_item:
        fecha.append((l.find('time').text.strip()))
        titulo.append(l.find('h3',{'class':'list-item__title'}).text.strip())
        desc.append(l.find('p').text.strip())
# %%
df['fecha'] = fecha
df['titulo'] = titulo
df['descripcion'] = desc
# %%
# Exportar los datos a un csv
df.to_csv('./data/{}_elcomercio.csv'.format(tags['tag']),sep=',')

