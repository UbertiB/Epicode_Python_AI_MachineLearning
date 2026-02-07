"""
Matplotlib è una delle librerie più potenti per la visualizzazione dei dati. E' completamente
integrata con librerie scientifiche come numpy e pandas. Offre due modalità principali di 
utilizzo:
1) Pyplot api (as plt) comoda per grafici veloci
2) Object oriented api, permeetto un controllo completo dei grafici. Preferibile in contesti avanzati.

Quando si lavora con df di grandi dimensioni, matplotlib si integra con pandas e numpy. i df pandas possono essere
visualizzati direttamente con plot.
Inoltre l'utilizzo di array np indicizzati, permette di costruire grafici estremamente efficienti, migliorando
le prestazioni.
Matplotlib supporta grafici di tipo lineare, scatter, barre, istogrammi, boxplot, grafici a torta, grafici 3D, 
superfici ed headmap.
Oltre alla creazione di grafici base, offre stumenti per la personalizzazione completa (colori, palette, 
stili di linea marker, trasparenza, colormap condizionali ed annotazioni dinamiche).

Un concetto chiave è la separazione tra logica dei dati e logica di visualizzazione.
In ambiente reale i dati subiscono trasformazioni multiple, aggregazioni, merge, creazione di feature temporali
o categorie, normalizzazioni, e imputazioni.
Matplotlib permette di utilizzare direttamente i risultati di questi papline come input per essere visualizzati
immediatamente.
La gestione di figure multisubplot consente di confrontare visivamente più metriche categorie simultaneamente.
Matplotlib supporta gridspec o subplots

L'approccio modulare e riutilizzabile, funzioni o classi dedicati alla generazioni di classi possono accettare
dati in imput restituendo grafici.
Questo riduce duplicazioni di codice, e facilità di aggiornamenti.

Matplotlib non è solo una libreria per creare grafici ma uno strumento professionale per la visualizzazione
dei dati avanzata


matplotlib ha degli stili predefiniti che cambiano da versione a versione. 
Quelli classici sono:
- default
- classic
- ggplot
- seaborn-v0_8 (non è di seaborn, è di matplotlib, spesso vecchi stili)
- bmh
- fast
- dark_background
- grayscale
- tableau-colorblind10

Si possono anche creare stili personalizzati (magari con colori aziendali) partendo da uno stile default
"""

#UTILIZZO DEGLI STILI PREDEFINITI IN MATPLOTLIB

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


dates=pd.date_range("2023-01-01",periods=30)
sales=np.random.randint(50,200,size=30)
df=pd.DataFrame({
    "date":dates,
    "sales":sales
}).set_index("date")

fix,ax=plt.subplots(figsize=(10,5))
ax.plot(df.index, df["sales"],color="blue",linestyle="-",marker="o",label="Vendite giornaliere")
ax.set_title("Vendite giornaliere gennaio 2023")
ax.set_xlabel("Data")
ax.set_ylabel("Vendite")
ax.grid(True)
ax.legend() 
plt.show()


input_values=[1,2,3,4,5]
squares=[1,4,9,16,25]
plt.style.use('tableau-colorblind10')  #IMPOSTO STILE PREDEFINITO
fig,ax=plt.subplots()
ax.plot(input_values,squares,linewidth=3)
ax.set_title("Square Numbers",fontsize=24)  
ax.set_xlabel("Value",fontsize=14)
ax.set_ylabel("Square of Value",fontsize=14)
ax.scatter(2,4,)  #EVIDENZIO UN PUNTO SPECIFICO

plt.show()

#elenco stili predefiniti:
print(plt.style.available)
#per vedere i files di configurazione (.mplstyle):
import matplotlib
print(matplotlib.get_configdir())
#per vedere lo stile in  uso:
plt.style.use("tableau-colorblind10")

forecast=df["sales"]*np.random.uniform(0.9,1.1,size=len(df))
df["forecast"]=forecast

fig,ax=plt.subplots(figsize=(10,6))
ax.plot(df.index,df["sales"],color="blue",marker="o",label="Vendite reali")
ax.plot(df.index,df["forecast"],color="orange",linestyle="--",label="Forecast")
ax.fill_between(df.index,df["sales"],color="gray",alpha=0.2)
ax.set_title("Confronto vendite reali vs Foreacst")
ax.set_xlabel("Data")
ax.set_ylabel("Vendite")
ax.grid("True")
ax.legend()
plt.show()

#
# DASHBOARD CON + GRAFICI
#

df["revenue"]=df["sales"]*np.random.randint(10,20,size=len(df))
df["units"]=np.random.randint(5,15,size=len(df))

fig,axs=plt.subplots(2,2,fig=(12,8))

axs[0,0].plot(df.index,df["sales"],color="blue") #in alto a sinistra
axs[0,0].set_title("Vendite")

axs[0,1].bar(df.index,df["units"],color="green")
axs[0,1].set_title("Unita vendute")

axs[1,0].plot(df.index,df["revenue"],color="red")
axs[1,0].set_title("Fatturato")

axs[1,1].scatter(df["sales"],df["revenue"],color="purple")
axs[1,1].set_title("Vendite vs fatturato")

for ax in axs.flat:
    ax.grid(True)
    ax.tick_params(axis="x",rotation=45)

plt.tight_layout()
plt.show()







