# %%
from bs4 import BeautifulSoup
import requests
import pandas as pd

df = pd.DataFrame()
fecha = list()
titulo = list()
link = list()
# %%
for p in range(1,411):
    url = f"http://elmercioco.com/page/{p}/"
    print("Page:", p)
    page = requests.get(url,timeout=3.500)
    soup = BeautifulSoup(page.content, "html.parser")
    items = soup.find_all("div",{"class":"td-block-span6"})
# %%
    for i in items:
        fecha.append(i.time['datetime'].split('T')[0].strip())
        titulo.append(i.h3.a['title'].strip())
        link.append(i.h3.a['href'].strip())
#%%
df['fecha'] = fecha
df['titulo'] = titulo
df['link'] = link

df.to_csv("./data/fake_news_elmercioco.csv",sep=",")