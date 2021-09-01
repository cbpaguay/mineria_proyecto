# %%
import pandas as pd
from datetime import datetime as dt
import locale
locale.setlocale(locale.LC_ALL, 'esp_esp')

df = pd.read_csv('data/asalto_elcomercio.csv',index_col=['Unnamed: 0'])

# %%
df2 = pd.read_csv('data/robo_elcomercio.csv',index_col=['Unnamed: 0'])

# %%
df3 = pd.read_csv('data/robos_elcomercio.csv',index_col=['Unnamed: 0'])
#%%
df4 = pd.read_csv('data/asaltos_elcomercio.csv',index_col=['Unnamed: 0'])

#%%
df5 = pd.read_csv('data/robo_elextra.csv',index_col=['Unnamed: 0'])
date_str=list()
for d in df5["fecha"]:
    date  = dt.strptime(d, '%B %d, %Y')
    date_str.append(date.strftime('%d/%m/%Y'))

df5["fecha"] = date_str
del(date_str)
# %%
df6 = pd.read_csv('data/robos_elextra.csv',index_col=['Unnamed: 0'])
date_str=list()
for d in df6["fecha"]:
    date  = dt.strptime(d, '%B %d, %Y')
    date_str.append(date.strftime('%d/%m/%Y'))

df6["fecha"] = date_str
del(date_str)
# %%
df7 = pd.read_csv('data/asalto_elextra.csv',index_col=['Unnamed: 0'])
date_str=list()
for d in df7["fecha"]:
    date  = dt.strptime(d, '%B %d, %Y')
    date_str.append(date.strftime('%d/%m/%Y'))

df7["fecha"] = date_str
del(date_str)
# %%
df8 = pd.read_csv('data/asaltos_elextra.csv',index_col=['Unnamed: 0'])
date_str=list()
for d in df8["fecha"]:
    date  = dt.strptime(d, '%B %d, %Y')
    date_str.append(date.strftime('%d/%m/%Y'))

df8["fecha"] = date_str
del(date_str)
# %%
df9 = pd.read_csv('data/robo_eltelegrafo.csv',index_col=['Unnamed: 0'])
date_str=list()
for d in df9["fecha"]:
    date  = dt.strptime(d, '%d de %B de %Y %H:%M')
    date_str.append(date.strftime('%d/%m/%Y'))

df9["fecha"] = date_str
del df9['link']
del(date_str)
# %%
df10 = pd.read_csv('data/asalto_eltelegrafo.csv',index_col=['Unnamed: 0'])
date_str=list()
for d in df10["fecha"]:
    date  = dt.strptime(d, '%d de %B de %Y %H:%M')
    date_str.append(date.strftime('%d/%m/%Y'))

df10["fecha"] = date_str
del df10['link']
del(date_str)
# %%
frames = [df,df2,df3,df4,df5,df6,df7,df8,df9,df10]
result = pd.concat(frames)
result['is_fake'] = 0
result = result.reset_index(drop=True)
# %%
result.to_csv('./data/real_complete_dataset.csv',sep=',')
# %%
