"""
ESERCIZIO 1
* Caricare un dataset di grandi dimensioni e ottimizzare i tipi di dato, confrontando
l'uso di memoria prima e dopo la conversione
ESERCIZIO 2
* Leggeere un file CSV di grandi dimensioni in modalità chunk e calcolare una statistica
aggregata incrementale (media, somma, conteggio)
ESERCIZIO 3
* Integrare Pandas con Dask o Modin per eseguire un'operazione di groupby o aggregazione
parallela confrontando i tempi di esecuzione
ESERCIZIO 4
* Salvare il dataset ottimizzato in formato Parquet e confrontare la velocità di 
lettura con il formato CSV
"""

import pandas as pd
import numpy as np
import time
import dask.dataframe as dd
import gc
"""
ESERCIZIO 1
* Caricare un dataset di grandi dimensioni e ottimizzare i tipi di dato, confrontando
l'uso di memoria prima e dopo la conversione
"""
df=pd.DataFrame({
    "id":np.arange(3_000_000),
    "citta":np.random.choice(["Roma","Milano","Napoli","Crema","Torino"],3_000_000),
    "vendite": np.random.uniform(10,500,3_000_000),
    "sconto":np.random.uniform(0,0.3,3_000_000)
})
print(f"Uso di memoria iniziale: {df.memory_usage(deep=True).sum()/1e6}")
#cambio dei tipi
df["citta"]=df["citta"].astype("category")
df["vendite"]=df["vendite"].astype("float32")
df["sconto"]=df["sconto"].astype("float32")
print(f"Uso di memoria dopo conversione tipo: {df.memory_usage(deep=True).sum()/1e6}")

"""
ESERCIZIO 2
* Leggeere un file CSV di grandi dimensioni in modalità chunk e calcolare una statistica
aggregata incrementale (media, somma, conteggio)
"""
t0=time.perf_counter()
df=pd.read_csv("dati_grandi.csv")
t1=time.perf_counter()
print(f"Tempo lettura file csv: {(t1-t0)*1000:2f} ms")

t0=time.perf_counter()
#lettura in chunck
chunks=pd.read_csv("dati_grandi.csv",chunksize=100_000)
i=0
for chunk in chunks:
    i+=1
    media=chunk["valore"].mean()
    max=chunk["valore"].max()
    min=chunk["valore"].min()
    #print(f"Valori per chunck: ({i}) media: {media}, massimo: {max}, minimo: {min}")
t1=time.perf_counter()
print(f"Tempo lettura e aggregazioni in chunk: {(t1-t0)*1000:2f} ms")

"""
ESERCIZIO 3
* Integrare Pandas con Dask o Modin per eseguire un'operazione di groupby o aggregazione
parallela confrontando i tempi di esecuzione
"""

t0=time.perf_counter()
df_dd=dd.read_csv("dati_grandi.csv")
t1=time.perf_counter()
print(f"Tempo lettura file con DASK: {(t1-t0)*1000:2f} ms")

t0=time.perf_counter()
df_group=(df.groupby("categoria")["valore"].sum())
t1=time.perf_counter()
print(f"Tempo di aggregazione con Pandas puro: {(t1-t0)*1000:2f} ms")

t0=time.perf_counter()
df_dd_group=(df_dd.groupby("categoria")["valore"].sum().compute())
t1=time.perf_counter()
print(f"Tempo di aggregazione con DASK: {(t1-t0)*1000:2f} ms")

"""
ESERCIZIO 4
* Salvare il dataset ottimizzato in formato Parquet e confrontare la velocità di 
lettura con il formato CSV
"""
t0=time.perf_counter()
df_p=pd.read_parquet("vendite_ottimizzato.parquest")
t1=time.perf_counter()
print(f"Tempo di lettura parquet: {(t1-t0)*1000:2f} ms")