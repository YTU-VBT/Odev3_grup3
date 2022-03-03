# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 20:40:50 2022

@author: Furkan
"""

import requests as rqs
from bs4 import BeautifulSoup as bfs
import re
import pandas as pd




nameff=[]

    

for  t in range(1,37):
    user = {"User-Agent":"Mozilla/5.0"}
    istek = rqs.get(f"https://www.epey.co.uk/monitor/e/TjtfczoxMDoiZml5YXQ6REVTQyI7=/{t}/",headers=user).content
    html = bfs(istek,"html.parser") 
    name=html.find_all("a",{"class":"urunadi"})
    for i in range(len(name)):
        nameff.append(name[i].text.replace(" ","-").lower())
    
    
    

veri=pd.DataFrame(columns=["marka","isim","ekran_b","piksel_s","tazeleme_h","ekran_t","tepki_s","parlaklık","fiyat"],index=range(len(nameff)))

j=0

while j<791:
    for z in nameff:

        istekin = rqs.get(f"https://www.epey.co.uk/monitor/{z}.html",headers=user).content   
        htmlin = bfs(istekin,"html.parser")
        ftrs=htmlin.find_all("div",{"class":"row row2"})
        fyt=htmlin.find_all("span",{"class":"hide kargodahil"})
        ism=htmlin.find_all("div",{"class":"baslik"})
        if j==791:
            break
        else:
        
            try:
                veri.loc[j]=[str(ism[0].text.split("\n")[1].split(" ")[0]),str(ism[0].text.split("\n")[1]),\
                             float(ftrs[0].text.split("i")[0]),\
                             str(ftrs[1].text.split("p")[0]),int(ftrs[2].text.split("H")[0]),\
                             str(ftrs[3].text.split("\n")[0]),float(ftrs[4].text.split("m")[0]),\
                             str(ftrs[5].text.split("c")[0]),float(fyt[0].text)]
                j+=1
                             
         
                 
            except (IndexError, ValueError) :
                pass

a=veri.value_counts()
df=veri.copy()
df.dropna(axis=0,inplace=True)   
df.drop_duplicates(inplace=True)

b=df.value_counts()
c=df.groupby(["piksel_s","ekran_t","tazeleme_h","marka"]).agg("count").unstack().T.fillna(value=0)

df.piksel_s.value_counts()
df.ekran_b.value_counts()
df.ekran_t.value_counts()
df.tazeleme_h.value_counts()
df.tepki_s.value_counts()
df.parlaklık.value_counts()       



import numpy as np
k=np.array(df.piksel_s.value_counts().index)
k.sort()
k1=np.array(df.tazeleme_h.value_counts().index)
k1.sort()
k2=np.array(df.tepki_s.value_counts().index).sort()

from pandas.api.types import CategoricalDtype
kk=list(k)
kk1=list(k1)
df.piksel_s=df.piksel_s.astype(CategoricalDtype(categories=kk ,ordered=True))
df.tazeleme_h=df.tazeleme_h.astype(CategoricalDtype(categories=kk1,ordered=True))
df.tepki_s=df.tepki_s.astype(CategoricalDtype(categories=k2,ordered=True)

                             
import seaborn as sns
import matplotlib.pyplot as plt

(sns
 .FacetGrid(df, 
               hue= "piksel_s",
               height = 7)
 .map(sns.kdeplot, "fiyat", shade=True)
 .add_legend()
);


sns.barplot(x="ekran_t", y="fiyat", data=df)
sns.catplot(x="tazeleme_h",y="fiyat",hue="ekran_t",kind="point", data=df, aspect=3 )
sns.catplot(x="tepki_s",y="fiyat",hue="ekran_t",kind="point", data=df, aspect=3 )
ax = sns.swarmplot(x="tepki_s", y="fiyat", data=df,hue="piksel_s")

df.to_excel("veri.xlsx")     
sss=pd.read_excel("veri.xlsx")
sss.drop(axis=1,inplace=True,columns="Unnamed: 0")
        