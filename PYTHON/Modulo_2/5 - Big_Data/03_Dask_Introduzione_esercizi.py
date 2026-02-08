"""
ESERCIZI 1
* Crea un dask dataframe a partire da un dataset csv di grandi dimensioni e confronta i tempi
di calcolo di una media per gruppo con pandas e dask
ESERCIZI 2
* leggere in parallelo più file csv e calcolare aggregazioni, visualizzando le partizioni gestire da dask
ESERCIZI 3
* Utilizzare dask array per generare un grande array casuale e confrontare i tempi di 
esecuzione tra i calcoli con numpy e con dask su operazioni come somma, media e 
deviazione standard.
"""

import pandas as pd
import numpy as np
import dask.dataframe as dd
import dask.array as da
import time
"""
ESERCIZI 1
* Crea un dask dataframe a partire da un dataset csv di grandi dimensioni e confronta i tempi
di calcolo di una media per gruppo con pandas e dask
"""

t0=time.perf_counter()
df_dask=dd.read_csv("dati_grandi.csv")
df_dask_group=(df_dask.groupby("categoria")["valore"].sum().compute())
t1=time.perf_counter()
print(f"Tempo di aggregazione con DASK: {(t1-t0)*1000:2f} ms")

t0=time.perf_counter()
df_pandas=pd.read_csv("dati_grandi.csv")
df_pandas_group=(df_pandas.groupby("categoria")["valore"].sum())
t1=time.perf_counter()
print(f"Tempo di aggregazione con pandas: {(t1-t0)*1000:2f} ms")

"""
ESERCIZI 2
* leggere in parallelo più file csv e calcolare aggregazioni, visualizzando le partizioni gestire da dask
"""

#lettura parallela di files multipli in parallelo
df=dd.read_csv("dati/vendite_*.csv")
totali=df.groupby("categoria")["valore"].sum().compute()
print(totali)
print("Numero partizioni:", df.npartitions)
print("Chiavi grafo:", list(df.dask.keys())[:10])
righe_per_partizione = df.map_partitions(len).compute()
print(righe_per_partizione)

"""
ESERCIZI 3
* Utilizzare dask array per generare un grande array casuale e confrontare i tempi di 
esecuzione tra i calcoli con numpy e con dask su operazioni come somma, media e 
deviazione standard.
"""
x=np.random.random((10_000,10_000))
dx=da.from_array(x,chunks=(1000,1000))
t1=time.time()
somma, media, std = da.compute(dx.sum(), dx.mean(), dx.std())
print(f"Dask somma: {somma}, media: {media}, deviazione standard: {std}")
t2=time.time()
print(f"tempo di esecuzione: {t2-t1:.3f} s")


t1=time.time()
somma=x.sum()
media=x.mean()
std=x.std()
print(f"Dask somma: {somma}, media: {media}, deviazione standard: {std}")
t2=time.time()
print(f"tempo di esecuzione: {t2-t1:.3f} s")




