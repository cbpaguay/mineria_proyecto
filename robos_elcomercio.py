# %%
from bs4  import  BeautifulSoup
import requests
import pandas as pd
#%% [markdown]
## WEB SCRAPING ROBOS EL COMERCIO
df = pd.DataFrame()
fecha = list()
titulo = list()
desc = list()
# %%
for i in range(1,35): # actualmente son 34 paginas
    url = "https://www.elcomercio.com/tag/robos/page/{}/".format(i)
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
df.to_csv('./data/robos_elcomercio.csv',sep=',')

