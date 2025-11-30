import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

# ** IDENTIFICARE ERRORI NEI DATI ** (celle vuote, valori icongruenti) e la loro gestione
"""
VALORI MANCANTI
Nessun data reale è perfetto, spesso troviamo valori mancanti
rappresentati da NONE 
la loro presenza falsa statistiche, impedire calcoli matematici
pandas di mette a disposizione degli strumenti per identificare i mancanti e contarli 
per stimare l'impatto sui dati, per definire poi la strategia per gestirli
1) primo approccio, CANCELLARLI
      però perdo informazoini e può instrodurre distorsioni
      scelta rapida ma rischiosa
2) altrimenti posso sostiuire valori mancanti con un COSTANTI arbitraria (utilizzo di costante tipo 0 o etichette generiche), 
      ma introduce un'informazione fittizia
3) altroapporccio, imputazione basata su MISURE STATISTICHE
      stimederivate da dati stessi, per esempio media (per varianti numeriche) o mediana (preferibile per dati con estermi), 
      per le variabili categorica la scelta è la moda (categoria più frequente)
      quese tecniche appiattiscono la variabilità dei dati 
      perchè sostituiscono i mancanti sempre con lo stesso valore mancante
4) altretecniche basate su ALGORITMI MACHINE LEARNING (che guarda relazioni tra variabili) 
      ess nnimputer, oppure regressione, oppure iterative imputer
      Necessarie quando i mancanti sono tanti ed impattanti sui dati.
      Non sostituisco con un valore uguale per tutti i mancanti, per contestualizzando il dato
      cercando di recuperare relazioni tra dati
      Mantengono la struttura statistica dei dati, ma richiedono più risorse computazinali
"""
#
# IDENTIFICAZIONE VALORI NULLI 
#
data={"Nome": ["Anna","Luca","Marta", "Paolo"],
      "Eta":[23, None, 29,35],
      "Citta": ["Roma","Milano",None,"Tornio"]}
df=pd.DataFrame(data)

#Identificazione valori nulli
print(df.isna().sum())

#
# GESTIONE VALORI NULLI
#

# 1) Sostituzione metodi matematici o statistici (stesso valore per tutti i mancanti)

#media
df["Eta"]=df["Eta"].fillna(df["Eta"].mean())
#stringa costante
df["Citta"]=df["Citta"].fillna("Sconosciuta")

print(df)

data1={"Reddito":[25000,32000,None,58000,None,45000]}
df1=pd.DataFrame(data1)

#MEDIANA
df1["Reddito"]=df1["Reddito"].fillna(df1["Reddito"].median())
print(df1)

# 2) Sostituzione metodi più complessi (non lo stesso valore per tutti i mancanti)

data2={"Altezza":[170,165,np.nan,180,175],
       "Peso":[65,np.nan,70,80,75]}
df2=pd.DataFrame(data2)

#KNNImputer (usa gli elementi più simili e vicini agli elementi mancanti per stimare il loro valore)
imputer=KNNImputer(n_neighbors=2) #elementi più simili e vicini ai dati mancanti per stimar eil loro valore
df2_imputer=pd.DataFrame(imputer.fit_transform(df2),columns=df2.columns) #columns=df2.columns serer per non perdere il nome originale delle colonne
print(f"Situazione originale: \n{df2}")
print(f"Situazione corretta: \n{df2_imputer}")