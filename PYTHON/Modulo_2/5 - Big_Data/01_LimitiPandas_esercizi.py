"""
ESERCIZIO 1
* Leggere un dataset di grandi dimensioni utilizzando chuncksize e calcolare stitistiche su ogni blocco
ESERCIZIO 2
* Convertire un df in formato Parquet e confrontare i tempi di lettura rispetto al formato csv
ESERCIZIO 3
* Ottimizzare i tipi di dati di un df per ridurre l'uso di memoria
ESERCIZIO 4
* Riprodurre le stesse operazioni con Dask e confrontare le pretazioni con Pandas
"""

import pandas as pd
import numpy as np
import dask.dataframe as dd
"""
ESERCIZIO 1
* Leggere un dataset di grandi dimensioni utilizzando chuncksize e calcolare stitistiche su ogni blocco
"""
#lettura in chunck
chunks=pd.read_csv("dati_grandi.csv",chunksize=100_000)
i=0
for chunk in chunks:
    i+=1
    media=chunk["valore"].mean()
    max=chunk["valore"].max()
    min=chunk["valore"].min()
    print(f"Valori per chunck: ({i}) media: {media}, massimo: {max}, minimo: {min}")

"""
ESERCIZIO 2
* Convertire un df in formato Parquet e confrontare i tempi di lettura rispetto al formato csv    
"""
import time
t0=time.perf_counter()
df=pd.read_csv("dati_grandi.csv")
t1=time.perf_counter()
print(f"Tempo lettura file csv: {(t1-t0)*1000:2f} ms")
df.to_parquet("dati_grandi_parquet")
t0=time.perf_counter()
df_p=pd.read_parquet("dati_grandi_parquet")
t1=time.perf_counter()
print(f"Tempo lettura file parquet: {(t1-t0)*1000:2f} ms")

"""
ESERCIZIO 3
* Ottimizzare i tipi di dati di un df per ridurre l'uso di memoria
"""
df=pd.read_csv("dati_grandi.csv")
mem = df.memory_usage(deep=True)
print(f"memoria utilizzata PRIMA della conversione dei tipi: \n{mem.sum() / 1024**2:.2f} MB")
df["categoria"]=df["categoria"].astype("category")
df["id"]=df["id"].astype("int32")
mem = df.memory_usage(deep=True)
print(f"memoria utilizzata DOPO della conversione dei tipi: \n{mem.sum() / 1024**2:.2f} MB")

"""
ESERCIZIO 4
* Riprodurre le stesse operazioni con Dask e confrontare le pretazioni con Pandas
"""
t0=time.perf_counter()
df_dd=dd.read_csv("dati_grandi.csv")
t1=time.perf_counter()
print(f"Tempo lettura file con DASK: {(t1-t0)*1000:2f} ms")
t0=time.perf_counter()
media=df_dd["valore"].mean().compute()
min=df_dd["valore"].min().compute()
max=df_dd["valore"].max().compute()
print(f"Valori per DASK media: {media}, massimo: {max}, minimo: {min}")
t1=time.perf_counter()
print(f"Tempo totale DASK (calcolo valori): {(t1-t0)*1000:2f} ms")
