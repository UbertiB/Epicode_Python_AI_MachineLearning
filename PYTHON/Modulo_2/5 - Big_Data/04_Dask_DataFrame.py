"""
DASK DATAFRAME
Dask dataframe è una parte della libreria pandas, progettata per gestire dataset di grandi dimensioni
che superano la capacità di memoria del singolo computer
Suddivide un grande dataset in molteplici partizioni più piccole ognuna delle quali è un normale dataframe 
pandas. Queste partizioni vengono elaborate in parallelo.
Dask permette di lavorare con dastaset tropppo grandi per essere caricati interamente in ram, mantenendo
la stessa semplicità sintattica di pandas.
l'obbiettivo principale è offire una soluzione scalabile che permetta di passare da un lavoro locale (pandas)
ad un lavoro distribuito (dask) senza dover riscrivere il codice.
L'architettura si basa su due elementi pricipali
- dask scheduler: si occupa di gestire ed eseguire le operazioni in modo parallelo ed efficiente
- dask graph: rappresenta la sequenza di operazioni da eseguire sui dati sotto forma di grafo
le oprazioni non vengono eseguite immediamente ma solo quando si rischiede un risultato esplicito come stampa
o grafico.
Dask è compatibile nativamente con pandas, quandi si possono applicare le stesse funzioni di pandas ma
in modo distribuito, consentendo una transizione quasi trasparente.
Le funzioni più comuni, sono tutte disponibili con la stessa sintassi.
Il codice rimane invariato
Le operazioni vengono distribuite sulle varie partizioni producendo lo stesso output di pandas.
Inoltre Dask fornisce metodi specifici per controllare il comportamento distribuito come repartition 
persit e compute che permettono di gestire la memoria e l'esecuzione del grafo.
Il vantaggio più evidente è la scalabilità è possibile elaborare dataset di dimensioni superiori alla memoria
disponibile, può essere eseguito sia in locale che su cluster distribuiti
L'interfaccia dask ml estende la capacità di calcolo parallelo anche al ml

Minore di 1GB - Pandas
tra 1 GB e 10 GB - Dask
olre 100 GB - Spark
Analisi distribuita python-native - Dask

"""
import dask.dataframe as dd
import pandas as pd
import time

#caricamente ed aggregazione distribuita
df=dd.read_csv("dati_grandi.csv") #dask costriusce solo un grafico di calcolo e non esegure l'operazione
risultati=df.groupby("categoria")["valore"].mean().compute() #compute per eseguire l operazione (forzo l'esecuzione parallela del calcolo)
print(risultati)

#salvataggio in formato efficiente (parquet)
df=dd.read_csv("dati_grandi.csv")
df.to_parquet("dati_parquet",compression="snappy") #salvo in formato efficiente per analisi future

#confronto pandas dask
t1=time.time()
df_pandas=pd.read_csv("dati_grandi.csv")
pandas_media=df_pandas["valore"].mean()
t2=time.time()

t3=time.time()
df_dask=dd.read_csv("dati_grandi.csv")
dask_media=df_dask["valore"].mean().compute()
t4=time.time()

print(f"Pandas: {t2-t1:.3f}s | Dask: {t4-t3:.3f}s")
#dask leggermente più lento perchè è uno strumento da utilizzarsi su big-data, in questo caso va bene Pandas

