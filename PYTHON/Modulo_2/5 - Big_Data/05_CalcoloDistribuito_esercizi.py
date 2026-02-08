"""
ESERCIZIO 1
* Carica un grande file csv, con dask e confronta i tempi di calcolo della media
utilizzando thread e process
ESERCIZIO 2
* Crea un client distirbuito e monitorare l'esecuzione dei task tramite dashboard web
ESERCIZIO 3
* Utilizzare persist() su un dataset grande e calcolare diverse statistiche,
osservando i miglioramenti di performance rispetto alla computazione standard
ESERCIZIO 4
* Visualizza e analizzare il grafo dei task di un operazione complessa per individuare 
possibili colli di bottiglia
"""
import pandas as pd
import numpy as np
import dask.dataframe as dd
import time
from dask.distributed import Client


def main():
    """
    ESERCIZIO 1
    * Carica un grande file csv, con dask e confronta i tempi di calcolo della media
    """    
    df=dd.read_csv("dati_grandi.csv")
    t0=time.time()
    media_trheades=df["valore"].mean().compute(scheduler="threads")
    t1=time.time()
    media_process=df["valore"].mean().compute(scheduler="processes")
    t2=time.time()

    print(f"media threads:{media_trheades} tempo: {t1-t0:.3f}s")
    print(f"media process:{media_process} tempo: {t2-t1:.3f}s")

def main2():
    """
    ESERCIZIO 2
    * Crea un client distirbuito e monitorare l'esecuzione dei task tramite 
    dashboard web
    """
    client=Client()
    print(client)
    print("Dashboard:", client.dashboard_link) 
    t0=time.time()
    df=dd.read_csv("dati_grandi.csv")
    media=df["valore"].mean().compute()
    t1=time.time()
    print(f"media client:{media} tempo: {t1-t0:.3f}s")
    client.close()

def main3():
    """
    ESERCIZIO 3
    * Utilizzare persist() su un dataset grande e calcolare diverse statistiche,
    osservando i miglioramenti di performance rispetto alla computazione standard    
    """
    client=Client()
    print(client)
    print("Dashboard:", client.dashboard_link) 
    t0=time.time()
    df=dd.read_csv("dati_grandi.csv")
    df_persist=df.persist()
    media_persist=df["valore"].mean().compute()
    t1=time.time()
    print(f"media persist:{media_persist} tempo: {t1-t0:.3f}s")
    client.close()

def main4():
    """
    ESERCIZIO 4
    * Visualizza e analizzare il grafo dei task di un operazione complessa per individuare 
    possibili colli di bottiglia
    """    

if __name__== "__main__":
    main()
    main2()
    main3()
    main4()
    