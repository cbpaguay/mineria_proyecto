# %%
from numpy import greater
import requests
from bs4 import BeautifulSoup
import pandas as pd
fecha = list()
titulo = list()
desc = list()
links = pd.read_csv('data/links_robo_eltelegrafo.csv')
i = 1
# %%
for l in links.link:
    url = 'https://www.eltelegrafo.com.ec' + l

    page = requests.get(url, timeout=30.500)  # obtengo la pagina entera
    soup = BeautifulSoup(page.content, 'html.parser')
    
    print('Pagina: ', i)

    for t in soup.find_all('h1',{'class':'story-heading'}):
        if(len(t.find_all('span')) > 0):
            titulo.append(t.find('span').text)

    v = soup.find('div',{'class':'itemFullText'})
    desc.append(v.find('p').text)

    fecha.append(soup.findAll('span',{'class':'story-publishup text-uppercase'})[0].text)

    i += 1


# %%
df = pd.DataFrame(columns=['fecha','titulo','descripcion'])
df['fecha'] = fecha
df['titulo'] = titulo
df['descripcion'] = desc
# %%
# Exportar los datos a un csv
df.to_csv('./data/robo_eltelegrafo.csv'.format(sep=','))
# %%
