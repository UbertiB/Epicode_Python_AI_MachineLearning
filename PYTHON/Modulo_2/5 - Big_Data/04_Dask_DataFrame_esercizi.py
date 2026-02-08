"""
ESERCIZIO 1
* Carica un grande file csv con dask e calcola una statistica aggregata distribuita (media o somma) 
confornta con pandas
ESERCIZIO 2
* Salvare il dataset in formato Parquet e verificare la differenza di tempo di lettura rispetto csv
ESERCIZIO 3
* Integra dask con scikit-learn per creare una pipline di preprocessing su dati di grandi dimensioni
e confrontare i tempi di esecuzione con l'equivalente in pandas
ESERCIZIO 4
*Visualizza il task graph di una computazione dask e interpretarne la struttura
"""

import pandas as pd
import numpy as np
import dask.dataframe as dd
import time

"""
ESERCIZIO 1
* Carica un grande file csv con dask e calcola una statistica aggregata distribuita (media o somma) 
confornta con pandas
"""
t1=time.time()
df_dask=dd.read_csv("dati_grandi.csv")
media=df_dask.groupby("categoria")["valore"].mean()
somma=df_dask.groupby("categoria")["valore"].sum()
media, somma = dd.compute(media, somma)   # <-- una sola compute
t2=time.time()
print(f"Dask: {t2-t1:.3f}s")

t1=time.time()
df_pandas=pd.read_csv("dati_grandi.csv")
media=df_pandas.groupby("categoria")["valore"].mean()
somma=df_pandas.groupby("categoria")["valore"].sum()
t2=time.time()
print(f"Pandas: {t2-t1:.3f}s")

"""
ESERCIZIO 2
* Salvare il dataset in formato Parquet e verificare la differenza di tempo di lettura rispetto csv
"""
df_dask.to_parquet("dati_grandi.parquet")

t1=time.time()
df_dask=dd.read_parquet("dati_grandi.parquet")
media=df_dask.groupby("categoria")["valore"].mean()
somma=df_dask.groupby("categoria")["valore"].sum()
media, somma = dd.compute(media, somma)   # <-- una sola compute
t2=time.time()
print(f"Dask: {t2-t1:.3f}s")

t1=time.time()
df_pandas=pd.read_parquet("dati_grandi.parquet")
media=df_pandas.groupby("categoria")["valore"].mean()
somma=df_pandas.groupby("categoria")["valore"].sum()
t2=time.time()
print(f"Pandas: {t2-t1:.3f}s")

"""
ESERCIZIO 3
* Integra dask con scikit-learn per creare una pipline di preprocessing su dati di grandi dimensioni
e confrontare i tempi di esecuzione con l'equivalente in pandas
"""