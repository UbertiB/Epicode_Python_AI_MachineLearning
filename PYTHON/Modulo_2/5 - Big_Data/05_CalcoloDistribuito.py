"""
CALCOLO DISTRIBUITO
Dask permette di sfrutare più core del processore 
senza richiedere modifiche sostanziali al codice scritto con pandas.
Il concetto chiave è quello di suddividere il lavoro in molteplici task indipendenti che 
vengono eseguite in parallelo e coordinate dalla scheduler di task
L'architettura di dask si base su 3 componenti principali:
1) Task graph
2) Scheduler
3) Partizioni dei dati
Ognioperazione è rappresentato come nodo, mentre gli archi le dipendenze tra le operazioni
Lo scheduler interpreta e decide cosa eseguire insieme e in quale ordine.
Ogni partizione è un df pandas indipendnete che può essere elaborato separatamente o in 
parallelo
Dask offre diversi tipi di scheduler:
- Single threaded (Sync Scheduler): esecuzione sequenziale utile per debug o esecuzioni
  semplici su un singolo core
- Threaded Scheduler: usa più thread in un singolo processo, buono per I/O-bound
- Multiprocessing Scheduler: ogni processo separato ed indipendente, utile per CPU-buond
- Distributed Scheduler: permette di gestire cluser di macchine
Ogni scheduler gestisce in modo diverso la concorenza comunicazione e la memoria.
In dask le operazioni sui dati vengono eseguite laty, cioè l'elaborazione è eseguita 
quando necessario tramite compute()
Lo scheduler bilancia i carichi di lavoro
Analizzare il grafo dei task permette di analizzare colli di bottiglia
Per ottenere prestazioni ottimali devono:
- Le partizioni dovrebbero essere abbastanza grandi da non creare oveload eccessivo ma
  non così grandi da saturare la memoria
- consigliabile utilizzare operazioni native pandas all'interno delle partizioni
- uso di persist per mantenere i dati in memori
- scrittura dei dati efficiente con Parquet per minimizzare tempi di i/o
- monitoraggio continuo con dasboard per controllare dinamicamente il carico

"""

import dask.dataframe as dd
from dask.distributed import Client

#calcolo distribuito con diversi scheduler
def main():
    df=dd.read_csv("dati_grandi.csv")
    media_trheades=df["valore"].mean().compute(scheduler="threads")
    media_process=df["valore"].mean().compute(scheduler="processes")
    print (media_trheades)
    print (media_process)

def main2():
    client=Client()
    df=dd.read_csv("dati_grandi.csv")
    somma=df["valore"].sum().compute()
    print(f"somma toale: {somma}")
    client.close()
def main3():
    client=Client()
    df=dd.read_csv("dati_grandi.csv")
    df=df.persist()
    media=df["valore"].mean().compute()
    somma=df["valore"].sum().compute()
    print(f"Somma: {somma} media:{media}")
    client.close()


if __name__== "__main__":
    main()
    main2()
    main3()


