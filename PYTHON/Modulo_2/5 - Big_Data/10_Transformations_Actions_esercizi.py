"""
ESERCIZIO 1
* Crea un datafram spark ed applica 3 trasformazioni (filter, select, withColumn) 
prima di un'action come .show() o count() per osservare la lazy evaluatione in azione
ESERCIZIO 2
* Carica un dataset CSV di grandi dimensioni e concatenare diverse trasformazioni, verificando
che l'esecuzione avvenga solo al momento dell'action finale
ESERCIZIO 3
* confronta le prestazioni di una narrow transformation e di una wide transformation, osservando la
differenza di tempo e di risorse utilizzate
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col,avg, count
import os
import pandas as pd
import time

#percorso per il worker
os.environ["PYSPARK_PYTHON"] = r"c:\users\uberti\.conda\envs\spark311\python.exe"
#percorso per il driver
os.environ["PYSPARK_DRIVER_PYTHON"] = r"c:\users\uberti\.conda\envs\spark311\python.exe"

"""
ESERCIZIO 1
* Crea un datafram spark ed applica 3 trasformazioni (filter, select, withColumn) 
prima di un'action come .show() o count() per osservare la lazy evaluatione in azione
"""

if False:
    spark=SparkSession.builder.appName("Esercizio1").getOrCreate()
    dati=[("A",10),("B",20),("C",30),("D",40),("A",50),("B",60),("C",70),("D",80)]
    df=spark.createDataFrame(dati,["categoria","valore"])
    #applico una transformation per filtrare i dati
    df_filtrato=df.filter(col("valore")>30)

    print(df_filtrato) #non viene eseguito nulla, è solo una descrizione del piano di esecuzione
    df_filtrato.show() #a questo punto vengono eseguite tutte le transformations precedenti e viene mostrato il risultato

    #applico una transformation per aggiungere una nuova colonna
    df_con_colonna=df_filtrato.withColumn("valore_doppio", col("valore")*2)
    #applico una transformation per selezionare le colonne
    df_selezionato=df_con_colonna.select("valore","valore_doppio")

    #applico un'azione per mostrare i risultati
    df_selezionato.show()
    spark.stop()

"""
ESERCIZIO 2
* Carica un dataset CSV di grandi dimensioni e concatenare diverse trasformazioni, verificando
che l'esecuzione avvenga solo al momento dell'action finale
"""

if False:
    spark=SparkSession.builder.appName("Transformations Actions").getOrCreate()
    df=spark.read.csv("dati_grandi.csv", header=True, inferSchema=True)
    #applico una transformation per filtrare i dati
    df_2=df.filter(col("valore")>100)
    df_3=df_2.select("categoria", "valore")
    df_4=df_3.groupBy("categoria").agg(count("valore").alias("conteggio"))
    #applico un'azione per mostrare i risultati dell'aggregazione
    df_4.show()
    spark.stop()

"""
ESERCIZIO 3
* confronta le prestazioni di una narrow transformation e di una wide transformation, osservando la
differenza di tempo e di risorse utilizzate
"""
if True:
    spark=SparkSession.builder.appName("NarrowWide").getOrCreate()
    dati=[("A",10),("B",20),("C",30),("D",40),("A",50),("B",60),("C",70),("D",80)]
    df=spark.createDataFrame(dati,["categoria","valore"])
    
    # Narrow transformation: withColumn
    t0 = time.time()
    df_mappato=df.withColumn("valore_doppio", col("valore")*2)
    df_mappato.show()
    t1 = time.time()
    print(f"Tempo per narrow transformation: {t1 - t0} secondi")

    # Wide transformation: groupBy e agg
    t0 = time.time()
    df_aggregato=df_mappato.groupBy("categoria").agg(avg("valore_doppio").alias("media_valore_doppio"))
    df_aggregato.show()
    t1 = time.time()
    print(f"Tempo per wide transformation: {t1 - t0} secondi")

    spark.stop()
