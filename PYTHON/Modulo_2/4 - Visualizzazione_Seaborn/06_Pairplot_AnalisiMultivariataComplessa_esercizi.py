"""
ESERCIZIO 1
* Creare un pairplot di un dataset a scelta, osservando le correlazioni 
tra le variabili numeriche

ESERCIZIO 2
* Aggiungere il parametro hue per distinguere categorie e confrontare la
distribuzione dei gruppi

ESERCIZIO 3
* Usare corne=True e diag_kind='kde' per miglioare la leggilità del grafico

ESERCIZIO 4
* Applicare una riduzione dimensionale con PCA e generare un pairplot
sulle componenti principali

"""

import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

df = sns.load_dataset("penguins")
print(df.head())

#pulizia minima
df=df.dropna().reset_index(drop=True)

#
#ESERCIZIO 1 - PAIRPLOT BASE
#
sns.pairplot(df) #crea una griglia discatterplot ed istogrammi che dimostrano tutte le correlazioni possibile tra le variabili numeriche del df
plt.suptitle("Pairplot base (dataset penguins)",y=1.02)
plt.show()

#flipper_lenght - body_mass mostrano una forte correlazione positiva
#bill_lenght - bill_depth mostrano  una relazione debole poco chiara
#bill_lenght - flipper_lenght

#
#ESERCIZIO 2 -PAIRPLOT CON HUE
#

#sono presenti 3 variabili categoriche tutte possibili utilizzarle con hue, 
#hue per essere chiaro, deve essere analizzato con una sola variabile per volta, lasciando 
#le altra categorie ad analisi successive.
sns.pairplot(df,hue="species") #crea una griglia discatterplot ed istogrammi che dimostrano tutte le correlazioni possibile tra le variabili numeriche del df
plt.suptitle("Pairplot con hue=species (dataset penguins)",y=1.02)
plt.show()

#l'introduzione della variabile specie (con hue) ha evidenziato come la specia rappresenta una variabile
#chiave nella struttura dei dati. Bill_lengh e boll_dept (che nell'esercizio 1 mostravano una relazione debole)
#mostrano di essere utili per distinguere la specie
#Flipper_lenght e body_mass confermano la loro forte correlazione con elevate capacità discriminatorie

#
#ESERCIZIO 3 - cornet + kde
#
sns.pairplot(df,diag_kind="kde",hue="species",corner=True)
plt.suptitle("Pairplot con hue=species (dataset penguins)",y=1.02)
plt.show()

#
#ESERCIZIO 4 - riduzione dimensionale con PCA
#
#1) Seleziono solo le variabili numeriche con .drop elimino le categoriche
#X = df.drop(["species","sex","island"], axis=1) 
X = df.select_dtypes(include="number")
#2) Standarizzazione (in modo da rendere le variabili confrontabili tra loro)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
#3) PCA iniziale per decidere quante componenti tenere
pca = PCA()
pca.fit(X_scaled)
print(pca.explained_variance_ratio_)
print(pca.explained_variance_ratio_.cumsum())
#dal risultato decido di tenere 3 PC (cerco sempre di superare il 90%)
#4) PCA finale con SOLO 3 componenti (decisione motivata dai due print precedenti)
pca = PCA(n_components=3)
components = pca.fit_transform(X_scaled)
#5) DataFrame PCA
df_pca = pd.DataFrame(components, columns=["PC1", "PC2", "PC3"])
df_pca["species"] = df["species"]
df_pca["island"] = df["island"]
df_pca["sex"] = df["sex"]
#6) Pairplot sulle componenti principali
sns.pairplot(df_pca, hue="species", diag_kind="kde", palette="coolwarm")
plt.suptitle("Pairplot sulle componenti principali (PC1, PC2,PC3)", y=1.02)
plt.show()


