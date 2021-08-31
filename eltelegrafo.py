# %%
from numpy import greater
import requests
from bs4 import BeautifulSoup
import pandas as pd
fecha = list()
titulo = list()
desc = list()
df = pd.read_csv('data/robo_eltelegrafo.csv',index_col=['Unnamed: 0'])
i = 1
# %%
for l in df.link:
    url = 'https://www.eltelegrafo.com.ec' + l

    page = requests.get(url, timeout=30.500)  # obtengo la pagina entera
    soup = BeautifulSoup(page.content, 'html.parser')
    
    print('Pagina: ', i)

    v = soup.find('div',{'class':'itemFullText'})
    desc.append(v.find('p').text)

    fecha.append(soup.findAll('span',{'class':'story-publishup text-uppercase'})[0].text)

    i += 1


# %%
df['fecha'] = fecha
df['descripcion'] = desc
# %%
# Exportar los datos a un csv
df.to_csv('./data/robo_eltelegrafo.csv',sep=',')
# %%
