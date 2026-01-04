"""
ESERCIZIO 1
* genera 3 serie temporali con trend differenti e rumore casuale usanto numpy
* inseriscile in un df pandas
* calcola media mobile e deviazione standard su finestra di 7 e 14 giorni
* visualizza tutte le serie in un unico grafico con linee, market, bande di deviazione

ESERCIZIO 2
* simula vendite giornaliere di 5 prodotti per 3 mesi
* usa pandas per aggregare settimanalmente e calcolare percentuale di variazione settimana-su-settimana
* visualizza in grafico combinato con linne plot colorati e annotazioni sui picchi di vendite

ESERCIZIO 3
* genera una matrice di correlazione di 6 variabili usando np
* visualizza la matrice come headmap, aggiungendo annotazioni numeriche, marker per valori>0.85 
e una colorbar personalizzata
* commenta pattern, valori e correlazoni interessanti

ESERCIZIO 4
* combina  linee plot, scatter plot e headmap in un unico script
* usa dati sintetici: vendite, temperatura giornaliera e numero di ordini
* evidenzia trend, anomalie e correlazioni tra variabili
* salva il grafico in formato png ed alta risuluzione e pdf

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#
#ESERCIZIO 1
#
giorni=pd.date_range("2025-01-01","2025-01-05",freq="D")
s1 = np.linspace(50,100,len(giorni)) + np.random.normal(0,5,len(giorni))
s2 = np.linspace(20,60,len(giorni)) + np.random.normal(0,8,len(giorni))
s3 = 80 + 10*np.sin(np.linspace(0,6*np.pi,len(giorni))) + np.random.normal(0,3,len(giorni))
df=pd.DataFrame({"S1":s1,"S2":s2,"S3":s3})
#print(df)

# Medie mobili e deviazione standard
for col in df.columns:
    df[f"{col}_MA7"] = df[col].rolling(7, min_periods=1).mean()
    df[f"{col}_STD7"] = df[col].rolling(7, min_periods=1).std()
    df[f"{col}_MA14"] = df[col].rolling(14, min_periods=1).mean()
    df[f"{col}_STD14"] = df[col].rolling(14, min_periods=1).std()
#print(df)

# Grafico con bande di deviazione
fig,ax=plt.subplots(figsize=(12,6))
ax.plot(df.index,df["S1"],color="blue",label="S1")
ax.plot(df.index,df["S1_MA7"],color="red",label="S1_MA7")
ax.fill_between(df.index,df["S1"],df["S1_MA7"],alpha=0.25)
ax.set_title("Serie temporali con media mobile")
ax.set_xlabel("quatita")
ax.set_ylabel("Valori")
ax.legend()

plt.tight_layout()
plt.show()


#
#ESERCIZIO 2
#

prodotti = [f"Prodotto {i}" for i in range(1,6)]
date = pd.date_range("2025-01-01", periods=90, freq='D')

quatita = np.random.randint(50,200, size=(90,5))
df = pd.DataFrame(quatita, columns=prodotti, index=date)

# Aggregazione settimanale
vendite_seettimanali = df.resample('W').sum()
#print(vendite_seettimanali)

# Percentuale variazione settimana-su-settimana
pct_change = vendite_seettimanali.pct_change()*100
print(pct_change)

# Grafico combinato
fig,ax=plt.subplots(figsize=(12,6))
for col in vendite_seettimanali.columns:
    ax.plot(vendite_seettimanali.index, vendite_seettimanali[col], marker='o', label=col)
    max_idx = vendite_seettimanali[col].idxmax()
    max_val = vendite_seettimanali[col].max()
    # Annotazioni sui picchi
    ax.annotate(f"{int(max_val)}", xy=(max_idx, max_val), xytext=(max_idx, max_val+10),
                 arrowprops=dict(facecolor='black', arrowstyle="->"))

ax.set_title("Vendite settimanali multi-prodotto con picchi evidenziati")
ax.set_xlabel("Settimana")
ax.set_ylabel("Unità vendute")
ax.legend()
plt.tight_layout()
plt.show()


#
# ESERCIZIO 3
#

np.random.seed(42)
df = pd.DataFrame(np.random.rand(100,6), columns=list("ABCDEF"))
#print(df)
corr_matrix = df.corr()

fig,ax=plt.subplots(figsize=(8,6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", cbar_kws={'label': 'Correlazione'})

# Marker per valori > 0.8
rows, cols = np.where(corr_matrix.values > 0.8)
print(rows)
for r,c in zip(rows, cols):
   ax.scatter(c+0.5, r+0.5, s=200, facecolors='none', edgecolors='black', linewidths=2)

ax.set_title("Heatmap correlazioni variabili con valori >0.8 evidenziati")
plt.show()

print("Analisi: valori elevati (>0.8) indicano forte correlazione tra alcune variabili, da considerare per possibili riduzioni dimensionali o insight di feature simili.")


#
# ESERCIZIO 4
#
np.random.seed(42)
dates = pd.date_range("2025-01-01", periods=30)
sales = np.random.randint(50,150,30)
temperature = np.random.uniform(10,30,30)
orders = np.random.randint(5,20,30)

fig, axs = plt.subplots(2,2, figsize=(12,10))

# Line plot vendite
axs[0,0].plot(dates, sales, color='blue', marker='o')
axs[0,0].set_title("Vendite giornaliere")

# Scatter temperature vs ordini
axs[0,1].scatter(temperature, orders, color='red')
axs[0,1].set_xlabel("Temperatura (°C)")
axs[0,1].set_ylabel("Ordini")
axs[0,1].set_title("Temperature vs Ordini")

# Heatmap vendite vs giorni vs ordini
data_heat = np.random.randint(0,20,(10,10))
sns.heatmap(data_heat, ax=axs[1,0], cmap='YlGnBu')
axs[1,0].set_title("Heatmap vendite/ordini (esempio)")

# Nascondo subplot vuoto
axs[1,1].axis('off')

plt.tight_layout()
plt.savefig("dashboard_sintetica.png", dpi=300)
plt.savefig("dashboard_sintetica.pdf")
plt.show()






