import requests
from bs4 import BeautifulSoup
import pandas as pd
titulo = list()
desc = list()
fecha = list()
# aplicar cada tag y el número de páginas
tags = {"tag":"robos","paginas":25}
# %%
for i in range(1,tags['paginas']): # actualmente son 142 paginas
    url = "https://www.extra.ec/search/{}/{}".format(tags['tag'],i)
    print("Page:",i)
    page = requests.get(url,timeout=3.500) # obtengo la pagina entera
    soup = BeautifulSoup(page.content, 'html.parser')
    list_item = soup.find_all("ul",{"class":"list con"}) # busco por la clase list-item
# %%
    for l in list_item:
        li = l.find_all("li") 
        for m in li:
            fecha.append((m.find('span').text.strip()))
            titulo.append(m.find('h1',{'class':'title'}).text.strip())
            desc.append(m.find('div',{'class':'epigraph'}).text.strip())
# %%
df = pd.DataFrame(columns=['fecha','titulo','descripcion'])
df['fecha'] = fecha
df['titulo'] = titulo
df['descripcion'] = desc
# %%
# Exportar los datos a un csv
df.to_csv('./data/{}_elextra.csv'.format(tags['tag']),sep=',')