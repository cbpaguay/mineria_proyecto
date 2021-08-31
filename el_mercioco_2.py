# %%
from bs4 import BeautifulSoup
import requests
import pandas as pd

df = pd.read_csv("./data/fake_news_elmercioco.csv",index_col=['Unnamed: 0'])
df.drop_duplicates(subset=['link'],inplace=True)
desc = list()
# %%
k = 0
for l in df.values:
    try:
        k += 1
        print("Page:",k)
        page = requests.get(l[2],timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        items = soup.find_all("div",{"class":"td-post-content"})
# %%
        for i in items:
            parr = i.find_all("p")
            desc.append((parr[0].text + " " + parr[1].text).strip())
    except Exception as e:
        print(e)
        desc.append("")

df['descripcion'] = desc
df.to_csv("./data/fake_news_elmercioco.csv",sep=",")